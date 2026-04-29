"""
API роуты для управления получателями.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import User, Recipient
from app.schemas.schemas import (
    RecipientCreate, RecipientResponse, RecipientUpdate,
)
from app.api.auth import get_current_user


router = APIRouter(prefix="/recipients", tags=["Recipients"])


@router.get("/", response_model=List[RecipientResponse])
def get_recipients(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить список получателей текущего пользователя."""
    recipients = (
        db.query(Recipient)
        .filter(Recipient.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return recipients


@router.post("/", response_model=RecipientResponse, status_code=status.HTTP_201_CREATED)
def create_recipient(
    recipient_data: RecipientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать нового получателя."""
    recipient = Recipient(
        user_id=current_user.id,
        **recipient_data.model_dump()
    )
    
    db.add(recipient)
    db.commit()
    db.refresh(recipient)
    
    return recipient


@router.get("/{recipient_id}", response_model=RecipientResponse)
def get_recipient(
    recipient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить информацию о получателе."""
    recipient = (
        db.query(Recipient)
        .filter(
            Recipient.id == recipient_id,
            Recipient.user_id == current_user.id
        )
        .first()
    )
    
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Получатель не найден"
        )
    
    return recipient


@router.put("/{recipient_id}", response_model=RecipientResponse)
def update_recipient(
    recipient_id: int,
    recipient_data: RecipientUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить информацию о получателе."""
    recipient = (
        db.query(Recipient)
        .filter(
            Recipient.id == recipient_id,
            Recipient.user_id == current_user.id
        )
        .first()
    )
    
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Получатель не найден"
        )
    
    update_data = recipient_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recipient, field, value)
    
    db.commit()
    db.refresh(recipient)
    
    return recipient


@router.delete("/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(
    recipient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить получателя."""
    recipient = (
        db.query(Recipient)
        .filter(
            Recipient.id == recipient_id,
            Recipient.user_id == current_user.id
        )
        .first()
    )
    
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Получатель не найден"
        )
    
    db.delete(recipient)
    db.commit()
    
    return None
