# Pydantic schemas for request/response validation

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums matching models
class UserRole(str, Enum):
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class SourceType(str, Enum):
    INSTAGRAM = "instagram"
    VK = "vk"
    TELEGRAM = "telegram"
    MANUAL = "manual"


class PostStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    USED = "used"


class MailingStatus(str, Enum):
    PENDING = "pending"
    PRINTED = "printed"
    SENT = "sent"
    RETURNED = "returned"


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_operator: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Plan schemas
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

    class Config:
        from_attributes = True


# Subscription schemas
class SubscriptionBase(BaseModel):
    plan_id: int
    is_auto_renew: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    status: Optional[SubscriptionStatus] = None
    is_auto_renew: Optional[bool] = None


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: SubscriptionStatus
    start_date: Optional[datetime]
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    is_auto_renew: bool
    cancelled_at: Optional[datetime]
    created_at: datetime
    plan: Optional[PlanResponse] = None

    class Config:
        from_attributes = True


# Source schemas
class SourceBase(BaseModel):
    source_type: SourceType
    external_id: Optional[str] = None


class SourceCreate(SourceBase):
    access_token: str
    refresh_token: Optional[str] = None
    token_expires: Optional[datetime] = None
    extra_data: Optional[dict] = None


class SourceUpdate(BaseModel):
    is_active: Optional[bool] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires: Optional[datetime] = None


class SourceResponse(SourceBase):
    id: int
    user_id: int
    is_active: bool
    last_synced_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# Recipient schemas
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


# SubscriptionRecipient schemas
class SubscriptionRecipientBase(BaseModel):
    subscription_id: int
    recipient_id: int
    emails_per_period: int = 1


class SubscriptionRecipientCreate(SubscriptionRecipientBase):
    pass


class SubscriptionRecipientResponse(BaseModel):
    id: int
    subscription_id: int
    recipient_id: int
    emails_per_period: int
    recipient: Optional[RecipientResponse] = None

    class Config:
        from_attributes = True


# Post schemas
class PostBase(BaseModel):
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    permalink: Optional[str] = None
    posted_at: Optional[datetime] = None


class PostCreate(PostBase):
    source_id: int
    external_id: str


class PostUpdate(BaseModel):
    status: Optional[PostStatus] = None


class PostResponse(PostBase):
    id: int
    source_id: int
    external_id: str
    status: PostStatus
    collected_at: datetime

    class Config:
        from_attributes = True


# Template schemas
class TemplateBase(BaseModel):
    name: str
    config: Optional[dict] = None


class TemplateCreate(TemplateBase):
    preview_image: Optional[str] = None


class TemplateResponse(TemplateBase):
    id: int
    preview_image: Optional[str] = None

    class Config:
        from_attributes = True


# Mailing schemas
class MailingBase(BaseModel):
    subscription_id: int
    recipient_id: int
    scheduled_date: Optional[datetime] = None


class MailingCreate(MailingBase):
    pass


class MailingUpdate(BaseModel):
    status: Optional[MailingStatus] = None
    tracking_number: Optional[str] = None
    label_url: Optional[str] = None


class MailingItemResponse(BaseModel):
    id: int
    post_id: int
    ordering: int
    template_id: Optional[int]
    generated_mockup_key: Optional[str]
    post: Optional[PostResponse] = None

    class Config:
        from_attributes = True


class MailingResponse(MailingBase):
    id: int
    status: MailingStatus
    tracking_number: Optional[str]
    label_url: Optional[str]
    created_at: datetime
    items: Optional[List[MailingItemResponse]] = []
    recipient: Optional[RecipientResponse] = None

    class Config:
        from_attributes = True


# Payment schemas
class PaymentBase(BaseModel):
    amount: float
    currency: str = "RUB"


class PaymentCreate(PaymentBase):
    subscription_id: Optional[int] = None


class PaymentResponse(PaymentBase):
    id: int
    user_id: int
    subscription_id: Optional[int]
    status: str
    yookassa_payment_id: Optional[str]
    created_at: datetime
    paid_at: Optional[datetime]

    class Config:
        from_attributes = True
