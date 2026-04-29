# Mailings router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.models import Mailing, User, Subscription
from ..schemas.schemas import MailingResponse, MailingCreate, MailingUpdate, MailingStatus
from ..core.security_jwt import get_current_user, get_current_operator_or_admin

router = APIRouter()


@router.get("/", response_model=List[MailingResponse])
async def list_mailings(
    skip: int = 0,
    limit: int = 100,
    subscription_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Mailing).join(Subscription).filter(Subscription.user_id == current_user.id)
    
    if subscription_id:
        query = query.filter(Mailing.subscription_id == subscription_id)
    
    mailings = query.offset(skip).limit(limit).all()
    return mailings


@router.get("/{mailing_id}", response_model=MailingResponse)
async def get_mailing(
    mailing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mailing = (
        db.query(Mailing)
        .join(Subscription)
        .filter(Mailing.id == mailing_id, Subscription.user_id == current_user.id)
        .first()
    )
    if not mailing:
        raise HTTPException(status_code=404, detail="Mailing not found")
    return mailing


@router.put("/{mailing_id}", response_model=MailingResponse)
async def update_mailing(
    mailing_id: int,
    mailing_update: MailingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_operator_or_admin)
):
    # Operators and admins can update any mailing
    mailing = db.query(Mailing).filter(Mailing.id == mailing_id).first()
    if not mailing:
        raise HTTPException(status_code=404, detail="Mailing not found")
    
    # Update fields
    if mailing_update.status is not None:
        mailing.status = mailing_update.status
    if mailing_update.tracking_number is not None:
        mailing.tracking_number = mailing_update.tracking_number
    if mailing_update.label_url is not None:
        mailing.label_url = mailing_update.label_url
    
    db.commit()
    db.refresh(mailing)
    
    return mailing


@router.post("/{mailing_id}/print")
async def mark_as_printed(
    mailing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_operator_or_admin)
):
    mailing = db.query(Mailing).filter(Mailing.id == mailing_id).first()
    if not mailing:
        raise HTTPException(status_code=404, detail="Mailing not found")
    
    mailing.status = MailingStatus.PRINTED
    
    db.commit()
    
    return {"message": "Mailing marked as printed", "mailing_id": mailing_id}


@router.post("/{mailing_id}/send")
async def mark_as_sent(
    mailing_id: int,
    tracking_number: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_operator_or_admin)
):
    mailing = db.query(Mailing).filter(Mailing.id == mailing_id).first()
    if not mailing:
        raise HTTPException(status_code=404, detail="Mailing not found")
    
    mailing.status = MailingStatus.SENT
    if tracking_number:
        mailing.tracking_number = tracking_number
    
    db.commit()
    
    return {"message": "Mailing marked as sent", "mailing_id": mailing_id}
