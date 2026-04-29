# Sources router (social media connections)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.models import Source, User
from ..schemas.schemas import SourceResponse, SourceCreate, SourceUpdate, SourceType
from ..core.security_jwt import get_current_user

router = APIRouter()


@router.post("/", response_model=SourceResponse)
async def create_source(
    source_data: SourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_source = Source(
        user_id=current_user.id,
        source_type=source_data.source_type,
        external_id=source_data.external_id,
        access_token=source_data.access_token,
        refresh_token=source_data.refresh_token,
        token_expires=source_data.token_expires,
        extra_data=source_data.extra_data,
    )
    
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    
    return new_source


@router.get("/", response_model=List[SourceResponse])
async def list_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sources = (
        db.query(Source)
        .filter(Source.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return sources


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    source = (
        db.query(Source)
        .filter(Source.id == source_id, Source.user_id == current_user.id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    source_update: SourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    source = (
        db.query(Source)
        .filter(Source.id == source_id, Source.user_id == current_user.id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    # Update fields
    if source_update.is_active is not None:
        source.is_active = source_update.is_active
    if source_update.access_token is not None:
        source.access_token = source_update.access_token
    if source_update.refresh_token is not None:
        source.refresh_token = source_update.refresh_token
    if source_update.token_expires is not None:
        source.token_expires = source_update.token_expires
    
    db.commit()
    db.refresh(source)
    
    return source


@router.delete("/{source_id}")
async def delete_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    source = (
        db.query(Source)
        .filter(Source.id == source_id, Source.user_id == current_user.id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db.delete(source)
    db.commit()
    
    return {"message": "Source deleted"}
