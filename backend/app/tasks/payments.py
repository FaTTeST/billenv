# Payment processing tasks
from celery import log
from datetime import datetime

from ..tasks import celery_app
from ..db.session import SessionLocal
from ..models.models import Subscription, Payment
from ..core.config import settings


@celery_app.task(bind=True, max_retries=3)
def process_subscription_payment(self, subscription_id: int):
    """Process recurring payment for a subscription"""
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return {"error": "Subscription not found"}
        
        if subscription.status != "active":
            return {"error": "Subscription is not active"}
        
        # Get plan price
        plan = subscription.plan
        amount = plan.price_per_month
        
        # In real implementation, call YooKassa API here
        # For now, simulate successful payment
        log.info(f"Processing payment {amount} RUB for subscription {subscription_id}")
        
        # Create payment record
        payment = Payment(
            user_id=subscription.user_id,
            subscription_id=subscription_id,
            amount=amount,
            currency="RUB",
            status="succeeded",  # Simulated
            paid_at=datetime.utcnow()
        )
        db.add(payment)
        
        # Extend subscription period
        if subscription.current_period_end:
            from datetime import timedelta
            new_end = subscription.current_period_end + timedelta(days=30)
        else:
            new_end = datetime.utcnow() + timedelta(days=30)
        
        subscription.current_period_start = subscription.current_period_end or datetime.utcnow()
        subscription.current_period_end = new_end
        
        db.commit()
        
        log.info(f"Payment processed successfully for subscription {subscription_id}")
        return {"success": True, "payment_id": payment.id}
    
    except Exception as exc:
        log.error(f"Error processing payment: {exc}")
        raise self.retry(exc=exc, countdown=300)
    finally:
        db.close()


@celery_app.task
def check_expiring_subscriptions():
    """Check and process subscriptions expiring soon"""
    db = SessionLocal()
    try:
        from datetime import timedelta
        
        # Find subscriptions ending in next 3 days with auto-renew
        expiring = db.query(Subscription).filter(
            Subscription.status == "active",
            Subscription.is_auto_renew == True,
            Subscription.current_period_end <= datetime.utcnow() + timedelta(days=3),
            Subscription.current_period_end >= datetime.utcnow()
        ).all()
        
        processed = 0
        for subscription in expiring:
            result = process_subscription_payment.delay(subscription.id)
            log.info(f"Queued payment for subscription {subscription.id}, task: {result.id}")
            processed += 1
        
        return {"subscriptions_processed": processed}
    
    except Exception as exc:
        log.error(f"Error checking expiring subscriptions: {exc}")
    finally:
        db.close()
