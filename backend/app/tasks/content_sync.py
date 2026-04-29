# Content synchronization tasks (Instagram, VK, Telegram)
from celery import log
from datetime import datetime, timedelta
import httpx

from ..tasks import celery_app
from ..db.session import SessionLocal
from ..models.models import Source, Post, SourceType
from ..core.config import settings


@celery_app.task(bind=True, max_retries=3)
def sync_instagram(self, source_id: int):
    """Sync posts from Instagram Graph API"""
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source or source.source_type != SourceType.INSTAGRAM:
            return {"error": "Source not found or invalid type"}
        
        # Determine since date
        since = source.last_synced_at or (datetime.utcnow() - timedelta(days=30))
        
        # Instagram Graph API endpoint
        access_token = source.access_token  # Should be decrypted in real impl
        instagram_id = source.external_id
        
        if not access_token or not instagram_id:
            return {"error": "Missing credentials"}
        
        url = f"https://graph.facebook.com/v18.0/{instagram_id}/media"
        params = {
            "fields": "id,media_type,media_url,permalink,timestamp,caption,thumbnail_url",
            "limit": 50,
            "access_token": access_token
        }
        
        with httpx.Client() as client:
            response = client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        
        posts_count = 0
        for item in data.get("data", []):
            timestamp = item.get("timestamp")
            if timestamp:
                posted_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            else:
                posted_at = datetime.utcnow()
            
            # Skip old posts
            if posted_at < since:
                continue
            
            # Check if post already exists
            existing = db.query(Post).filter(
                Post.external_id == item["id"],
                Post.source_id == source_id
            ).first()
            
            if existing:
                continue
            
            # Create new post
            new_post = Post(
                source_id=source_id,
                external_id=item["id"],
                media_type=item.get("media_type"),
                media_url=item.get("media_url"),
                thumbnail_url=item.get("thumbnail_url"),
                caption=item.get("caption"),
                permalink=item.get("permalink"),
                posted_at=posted_at,
                status="approved"  # Auto-approve in MVP
            )
            db.add(new_post)
            posts_count += 1
        
        # Update last synced time
        source.last_synced_at = datetime.utcnow()
        db.commit()
        
        log.info(f"Synced {posts_count} new Instagram posts for source {source_id}")
        return {"success": True, "posts_synced": posts_count}
    
    except Exception as exc:
        log.error(f"Error syncing Instagram: {exc}")
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()


@celery_app.task(bind=True, max_retries=3)
def sync_vk(self, source_id: int):
    """Sync posts from VK API"""
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source or source.source_type != SourceType.VK:
            return {"error": "Source not found or invalid type"}
        
        since = source.last_synced_at or (datetime.utcnow() - timedelta(days=30))
        access_token = source.access_token
        owner_id = source.external_id
        
        if not access_token or not owner_id:
            return {"error": "Missing credentials"}
        
        url = "https://api.vk.com/method/wall.get"
        params = {
            "owner_id": owner_id,
            "count": 100,
            "filter": "owner",
            "access_token": access_token,
            "v": "5.199"
        }
        
        with httpx.Client() as client:
            response = client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        
        if "error" in data:
            raise Exception(f"VK API error: {data['error']}")
        
        posts_count = 0
        for item in data.get("response", {}).get("items", []):
            if item.get("date"):
                posted_at = datetime.fromtimestamp(item["date"])
            else:
                continue
            
            if posted_at < since:
                continue
            
            # Skip posts without attachments
            attachments = item.get("attachments", [])
            photos = [a for a in attachments if a.get("type") == "photo"]
            if not photos:
                continue
            
            # Get highest resolution photo
            photo = photos[0].get("photo", {})
            media_url = photo.get("photo_2560") or photo.get("photo_1280") or photo.get("photo_807")
            
            existing = db.query(Post).filter(
                Post.external_id == str(item["id"]),
                Post.source_id == source_id
            ).first()
            
            if existing:
                continue
            
            new_post = Post(
                source_id=source_id,
                external_id=str(item["id"]),
                media_type="image",
                media_url=media_url,
                caption=item.get("text"),
                permalink=f"https://vk.com/wall{owner_id}_{item['id']}",
                posted_at=posted_at,
                status="approved"
            )
            db.add(new_post)
            posts_count += 1
        
        source.last_synced_at = datetime.utcnow()
        db.commit()
        
        log.info(f"Synced {posts_count} new VK posts for source {source_id}")
        return {"success": True, "posts_synced": posts_count}
    
    except Exception as exc:
        log.error(f"Error syncing VK: {exc}")
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()


@celery_app.task
def sync_all_sources():
    """Task to sync all active sources"""
    db = SessionLocal()
    try:
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        results = []
        for source in sources:
            if source.source_type == SourceType.INSTAGRAM:
                result = sync_instagram.delay(source.id)
                results.append({"source_id": source.id, "task_id": result.id})
            elif source.source_type == SourceType.VK:
                result = sync_vk.delay(source.id)
                results.append({"source_id": source.id, "task_id": result.id})
        
        return {"sources_synced": len(results), "tasks": results}
    finally:
        db.close()
