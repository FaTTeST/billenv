"""
Инициализация модуля schemas.
"""
from app.schemas.schemas import (
    # User
    UserBase, UserCreate, UserUpdate, UserResponse,
    # Auth
    Token, TokenData, LoginRequest,
    # Plan
    PlanBase, PlanCreate, PlanResponse,
    # Subscription
    SubscriptionBase, SubscriptionCreate, SubscriptionUpdate,
    SubscriptionRecipientBase, SubscriptionResponse,
    # Source
    SourceBase, SourceCreate, SourceUpdate, SourceResponse,
    # Recipient
    RecipientBase, RecipientCreate, RecipientUpdate, RecipientResponse,
    # Post
    PostBase, PostCreate, PostUpdate, PostResponse,
    # Mailing
    MailingBase, MailingCreate, MailingUpdate,
    MailingItemBase, MailingItemResponse, MailingResponse,
    # Payment
    PaymentBase, PaymentCreate, PaymentResponse,
    # Template
    TemplateBase, TemplateCreate, TemplateResponse,
    # Enums
    SourceTypeEnum, SubscriptionStatusEnum, PostStatusEnum,
    MailingStatusEnum,
)

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    # Auth
    "Token", "TokenData", "LoginRequest",
    # Plan
    "PlanBase", "PlanCreate", "PlanResponse",
    # Subscription
    "SubscriptionBase", "SubscriptionCreate", "SubscriptionUpdate",
    "SubscriptionRecipientBase", "SubscriptionResponse",
    # Source
    "SourceBase", "SourceCreate", "SourceUpdate", "SourceResponse",
    # Recipient
    "RecipientBase", "RecipientCreate", "RecipientUpdate", "RecipientResponse",
    # Post
    "PostBase", "PostCreate", "PostUpdate", "PostResponse",
    # Mailing
    "MailingBase", "MailingCreate", "MailingUpdate",
    "MailingItemBase", "MailingItemResponse", "MailingResponse",
    # Payment
    "PaymentBase", "PaymentCreate", "PaymentResponse",
    # Template
    "TemplateBase", "TemplateCreate", "TemplateResponse",
    # Enums
    "SourceTypeEnum", "SubscriptionStatusEnum", "PostStatusEnum",
    "MailingStatusEnum",
]
