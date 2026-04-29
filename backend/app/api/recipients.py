# Recipients router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.models import Recipient, User
from ..schemas.schemas import RecipientResponse, RecipientCreate, RecipientUpdate
from ..core.security_jwt import get_current_user

router = APIRouter()


@router.post("/", response_model=RecipientResponse)
async def create_recipient(
    recipient_data: RecipientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_recipient = Recipient(
        user_id=current_user.id,
        full_name=recipient_data.full_name,
        address_line=recipient_data.address_line,
        postal_code=recipient_data.postal_code,
        country=recipient_data.country,
        note=recipient_data.note,
    )
    
    db.add(new_recipient)
    db.commit()
    db.refresh(new_recipient)
    
    return new_recipient


@router.get("/", response_model=List[RecipientResponse])
async def list_recipients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipients = (
        db.query(Recipient)
        .filter(Recipient.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return recipients


@router.get("/{recipient_id}", response_model=RecipientResponse)
async def get_recipient(
    recipient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipient = (
        db.query(Recipient)
        .filter(Recipient.id == recipient_id, Recipient.user_id == current_user.id)
        .first()
    )
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return recipient


@router.put("/{recipient_id}", response_model=RecipientResponse)
async def update_recipient(
    recipient_id: int,
    recipient_update: RecipientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipient = (
        db.query(Recipient)
        .filter(Recipient.id == recipient_id, Recipient.user_id == current_user.id)
        .first()
    )
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Update fields
    if recipient_update.full_name is not None:
        recipient.full_name = recipient_update.full_name
    if recipient_update.address_line is not None:
        recipient.address_line = recipient_update.address_line
    if recipient_update.postal_code is not None:
        recipient.postal_code = recipient_update.postal_code
    if recipient_update.country is not None:
        recipient.country = recipient_update.country
    if recipient_update.note is not None:
        recipient.note = recipient_update.note
    if recipient_update.is_verified is not None:
        recipient.is_verified = recipient_update.is_verified
    
    db.commit()
    db.refresh(recipient)
    
    return recipient


@router.delete("/{recipient_id}")
async def delete_recipient(
    recipient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipient = (
        db.query(Recipient)
        .filter(Recipient.id == recipient_id, Recipient.user_id == current_user.id)
        .first()
    )
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    db.delete(recipient)
    db.commit()
    
    return {"message": "Recipient deleted"}
