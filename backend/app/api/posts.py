# Posts router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.models import Post, User, Source
from ..schemas.schemas import PostResponse, PostCreate, PostUpdate, PostStatus
from ..core.security_jwt import get_current_user

router = APIRouter()


@router.post("/", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify source belongs to user
    source = db.query(Source).filter(
        Source.id == post_data.source_id,
        Source.user_id == current_user.id
    ).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    new_post = Post(
        source_id=post_data.source_id,
        external_id=post_data.external_id,
        media_type=post_data.media_type,
        media_url=post_data.media_url,
        thumbnail_url=post_data.thumbnail_url,
        caption=post_data.caption,
        permalink=post_data.permalink,
        posted_at=post_data.posted_at,
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    skip: int = 0,
    limit: int = 100,
    source_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Post).join(Source).filter(Source.user_id == current_user.id)
    
    if source_id:
        query = query.filter(Post.source_id == source_id)
    
    posts = query.offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = (
        db.query(Post)
        .join(Source)
        .filter(Post.id == post_id, Source.user_id == current_user.id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = (
        db.query(Post)
        .join(Source)
        .filter(Post.id == post_id, Source.user_id == current_user.id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Update fields
    if post_update.status is not None:
        post.status = post_update.status
    
    db.commit()
    db.refresh(post)
    
    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = (
        db.query(Post)
        .join(Source)
        .filter(Post.id == post_id, Source.user_id == current_user.id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    
    return {"message": "Post deleted"}
