# Plans router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.models import Plan, User
from ..schemas.schemas import PlanResponse, PlanCreate
from ..core.security_jwt import get_current_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[PlanResponse])
async def list_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plans = db.query(Plan).filter(Plan.is_active == True).offset(skip).limit(limit).all()
    return plans


@router.post("/", response_model=PlanResponse)
async def create_plan(
    plan_data: PlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    # Check if slug already exists
    existing_plan = db.query(Plan).filter(Plan.slug == plan_data.slug).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Plan with this slug already exists")
    
    new_plan = Plan(**plan_data.model_dump())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    return new_plan


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
