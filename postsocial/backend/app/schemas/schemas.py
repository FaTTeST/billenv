"""
Pydantic схемы для валидации данных.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# === ENUM SCHEMAS ===
class SourceTypeEnum(str, Enum):
    INSTAGRAM = "instagram"
    VK = "vk"
    TELEGRAM = "telegram"
    MANUAL = "manual"


class SubscriptionStatusEnum(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PostStatusEnum(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    USED = "used"


class MailingStatusEnum(str, Enum):
    PENDING = "pending"
    PRINTED = "printed"
    SENT = "sent"
    RETURNED = "returned"


# === USER ===
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    is_operator: bool
    is_admin: bool
    
    class Config:
        from_attributes = True


# === AUTH ===
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# === PLAN ===
class PlanBase(BaseModel):
    name: str
    slug: str
    price_per_month: float
    mailing_count_per_month: int
    description: Optional[str] = None


class PlanCreate(PlanBase):
    pass


class PlanResponse(PlanBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# === SUBSCRIPTION ===
class SubscriptionBase(BaseModel):
    plan_id: int
    is_auto_renew: bool = True


class SubscriptionCreate(SubscriptionBase):
    start_date: datetime


class SubscriptionUpdate(BaseModel):
    status: Optional[SubscriptionStatusEnum] = None
    is_auto_renew: Optional[bool] = None


class SubscriptionRecipientBase(BaseModel):
    recipient_id: int
    emails_per_period: int = 1


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: SubscriptionStatusEnum
    start_date: datetime
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    is_auto_renew: bool
    cancelled_at: Optional[datetime] = None
    created_at: datetime
    plan: Optional[PlanResponse] = None
    recipients: Optional[List[SubscriptionRecipientBase]] = None
    
    class Config:
        from_attributes = True


# === SOURCE ===
class SourceBase(BaseModel):
    source_type: SourceTypeEnum
    external_id: Optional[str] = None


class SourceCreate(SourceBase):
    access_token: Optional[str] = None
    extra_data: Optional[dict] = None


class SourceUpdate(BaseModel):
    is_active: Optional[bool] = None
    access_token: Optional[str] = None


class SourceResponse(SourceBase):
    id: int
    user_id: int
    is_active: bool
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# === RECIPIENT ===
class RecipientBase(BaseModel):
    full_name: str
    address_line: str
    postal_code: str
    country: str = "Россия"
    note: Optional[str] = None


class RecipientCreate(RecipientBase):
    pass


class RecipientUpdate(BaseModel):
    full_name: Optional[str] = None
    address_line: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    note: Optional[str] = None
    is_verified: Optional[bool] = None


class RecipientResponse(RecipientBase):
    id: int
    user_id: int
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# === POST ===
class PostBase(BaseModel):
    external_id: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    permalink: Optional[str] = None
    posted_at: Optional[datetime] = None


class PostCreate(PostBase):
    source_id: int


class PostUpdate(BaseModel):
    status: Optional[PostStatusEnum] = None
    caption: Optional[str] = None


class PostResponse(PostBase):
    id: int
    source_id: int
    status: PostStatusEnum
    collected_at: datetime
    
    class Config:
        from_attributes = True


# === MAILING ===
class MailingItemBase(BaseModel):
    post_id: int
    ordering: int = 0
    template_id: Optional[int] = None


class MailingBase(BaseModel):
    subscription_id: int
    recipient_id: int
    scheduled_date: datetime


class MailingCreate(MailingBase):
    items: Optional[List[MailingItemBase]] = None


class MailingUpdate(BaseModel):
    status: Optional[MailingStatusEnum] = None
    tracking_number: Optional[str] = None
    label_url: Optional[str] = None
    sent_at: Optional[datetime] = None


class MailingItemResponse(BaseModel):
    id: int
    post_id: int
    ordering: int
    template_id: Optional[int] = None
    generated_mockup_key: Optional[str] = None
    post: Optional[PostResponse] = None
    
    class Config:
        from_attributes = True


class MailingResponse(MailingBase):
    id: int
    status: MailingStatusEnum
    tracking_number: Optional[str] = None
    label_url: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime
    items: Optional[List[MailingItemResponse]] = None
    
    class Config:
        from_attributes = True


# === PAYMENT ===
class PaymentBase(BaseModel):
    amount: float
    currency: str = "RUB"
    description: Optional[str] = None


class PaymentCreate(PaymentBase):
    subscription_id: Optional[int] = None


class PaymentResponse(PaymentBase):
    id: int
    user_id: int
    subscription_id: Optional[int] = None
    status: str
    yookassa_payment_id: Optional[str] = None
    created_at: datetime
    paid_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# === TEMPLATE ===
class TemplateBase(BaseModel):
    name: str
    config: dict
    preview_image: Optional[str] = None


class TemplateCreate(TemplateBase):
    pass


class TemplateResponse(TemplateBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
