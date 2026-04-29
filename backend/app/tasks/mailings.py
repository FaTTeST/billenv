# Mailing generation tasks
from celery import log
from datetime import datetime, timedelta
import os
from PIL import Image, ImageDraw, ImageFont

from ..tasks import celery_app
from ..db.session import SessionLocal
from ..models.models import Mailing, Post, Subscription, SubscriptionRecipient, MailingStatus
from ..core.config import settings


@celery_app.task(bind=True, max_retries=3)
def generate_mockup(self, mailing_id: int):
    """Generate mockup image for a mailing item"""
    db = SessionLocal()
    try:
        mailing_item = db.query(MailingItem).filter(MailingItem.id == mailing_id).first()
        if not mailing_item:
            return {"error": "Mailing item not found"}
        
        post = mailing_item.post
        if not post or not post.media_url:
            return {"error": "No media for post"}
        
        # Download image
        import httpx
        with httpx.Client() as client:
            response = client.get(post.media_url, timeout=30.0)
            response.raise_for_status()
        
        # Create A6 size image (1240x1748 px at 300 dpi)
        img = Image.new('RGB', (1240, 1748), color='white')
        
        # Load and resize photo
        from io import BytesIO
        photo = Image.open(BytesIO(response.content))
        photo.thumbnail((1140, 1200), Image.Resampling.LANCZOS)
        
        # Calculate position to center photo
        x = (1240 - photo.width) // 2
        y = 100
        img.paste(photo, (x, y))
        
        # Add caption if exists
        if post.caption:
            draw = ImageDraw.Draw(img)
            # Try to load a font, fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            max_width = 1100
            words = post.caption.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = f"{current_line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            # Draw text
            text_y = y + photo.height + 50
            for line in lines[:10]:  # Limit to 10 lines
                draw.text((70, text_y), line, fill='black', font=font)
                text_y += 35
        
        # Save mockup
        mockup_dir = os.path.join(settings.STORAGE_PATH, "mailings", str(mailing_item.mailing_id))
        os.makedirs(mockup_dir, exist_ok=True)
        
        mockup_path = os.path.join(mockup_dir, f"item_{mailing_item.id}.jpg")
        img.save(mockup_path, quality=90)
        
        # Update mailing item
        mailing_item.generated_mockup_key = mockup_path
        db.commit()
        
        log.info(f"Generated mockup for mailing item {mailing_id}")
        return {"success": True, "mockup_path": mockup_path}
    
    except Exception as exc:
        log.error(f"Error generating mockup: {exc}")
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()


@celery_app.task
def create_scheduled_mailings():
    """Create mailings for subscriptions due today"""
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        
        # Find active subscriptions with mailings due
        subscriptions = db.query(Subscription).filter(
            Subscription.status == "active",
            Subscription.current_period_end >= datetime.utcnow()
        ).all()
        
        created_count = 0
        for subscription in subscriptions:
            # Get recipients for this subscription
            sub_recipients = db.query(SubscriptionRecipient).filter(
                SubscriptionRecipient.subscription_id == subscription.id
            ).all()
            
            for sub_recipient in sub_recipients:
                # Check if mailing is due for this recipient
                # Simple logic: create one mailing per period per recipient
                existing = db.query(Mailing).filter(
                    Mailing.subscription_id == subscription.id,
                    Mailing.recipient_id == sub_recipient.recipient_id,
                    Mailing.scheduled_date >= today - timedelta(days=1),
                    Mailing.scheduled_date <= today + timedelta(days=1)
                ).first()
                
                if existing:
                    continue
                
                # Create new mailing
                mailing = Mailing(
                    subscription_id=subscription.id,
                    recipient_id=sub_recipient.recipient_id,
                    scheduled_date=datetime.utcnow(),
                    status=MailingStatus.PENDING
                )
                db.add(mailing)
                db.flush()
                
                # Get unused posts for this mailing
                used_post_ids = db.query(MailingItem.post_id).join(MailingItem).all()
                used_post_ids = [p[0] for p in used_post_ids]
                
                posts = db.query(Post).filter(
                    Post.source_id.in_(
                        db.query(Source.id).filter(Source.user_id == subscription.user_id)
                    ),
                    Post.status == "approved",
                    Post.id.notin_(used_post_ids) if used_post_ids else True
                ).order_by(Post.posted_at.desc()).limit(sub_recipient.emails_per_period).all()
                
                # Create mailing items
                for i, post in enumerate(posts):
                    mailing_item = MailingItem(
                        mailing_id=mailing.id,
                        post_id=post.id,
                        ordering=i
                    )
                    db.add(mailing_item)
                    
                    # Queue mockup generation
                    generate_mockup.delay(mailing_item.id)
                
                created_count += 1
        
        db.commit()
        log.info(f"Created {created_count} scheduled mailings")
        return {"success": True, "mailings_created": created_count}
    
    except Exception as exc:
        log.error(f"Error creating scheduled mailings: {exc}")
        raise self.retry(exc=exc, countdown=300)
    finally:
        db.close()


# Import needed here to avoid circular imports
from ..models.models import Source
