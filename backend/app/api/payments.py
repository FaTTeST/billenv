# Payments router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.models import Payment, User, Subscription
from ..schemas.schemas import PaymentResponse, PaymentCreate
from ..core.security_jwt import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    subscription_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Payment).filter(Payment.user_id == current_user.id)
    
    if subscription_id:
        query = query.filter(Payment.subscription_id == subscription_id)
    
    payments = query.offset(skip).limit(limit).all()
    return payments


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id, Payment.user_id == current_user.id)
        .first()
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/webhook/yookassa", response_model=dict)
async def yookassa_webhook(payment_data: dict, db: Session = Depends(get_db)):
    """
    Webhook endpoint for YooKassa payment notifications.
    In production, verify webhook signature.
    """
    # Extract payment info from webhook
    payment_id = payment_data.get("object", {}).get("id")
    payment_status = payment_data.get("event", "succeeded")
    
    if not payment_id:
        raise HTTPException(status_code=400, detail="Invalid webhook data")
    
    # Find payment in database
    payment = db.query(Payment).filter(Payment.yookassa_payment_id == payment_id).first()
    
    if payment:
        if payment_status == "payment.succeeded":
            payment.status = "succeeded"
            from datetime import datetime
            payment.paid_at = datetime.utcnow()
        elif payment_status == "payment.canceled":
            payment.status = "canceled"
        
        db.commit()
    
    return {"status": "ok"}
