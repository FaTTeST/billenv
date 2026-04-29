# SQLAlchemy models for PostSocial

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, JSONB, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..db.session import Base


class UserRole(str, enum.Enum):
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class SourceType(str, enum.Enum):
    INSTAGRAM = "instagram"
    VK = "vk"
    TELEGRAM = "telegram"
    MANUAL = "manual"


class PostStatus(str, enum.Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    USED = "used"


class MailingStatus(str, enum.Enum):
    PENDING = "pending"
    PRINTED = "printed"
    SENT = "sent"
    RETURNED = "returned"


class User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_operator = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="user")
    sources = relationship("Source", back_populates="user")
    recipients = relationship("Recipient", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Plan(Base):
    __tablename__ = "plans_plan"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    price_per_month = Column(Float, nullable=False)
    mailing_count_per_month = Column(Integer, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions_subscription"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans_plan.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime(timezone=True))
    current_period_start = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))
    payment_method_id = Column(String(255))
    is_auto_renew = Column(Boolean, default=True)
    cancelled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    recipients = relationship("SubscriptionRecipient", back_populates="subscription")
    mailings = relationship("Mailing", back_populates="subscription")
    payments = relationship("Payment", back_populates="subscription")


class Source(Base):
    __tablename__ = "sources_source"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)
    external_id = Column(String(255))
    access_token = Column(String(1024))  # Encrypted
    refresh_token = Column(String(1024))  # Encrypted
    token_expires = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime(timezone=True))
    extra_data = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="sources")
    posts = relationship("Post", back_populates="source")


class Recipient(Base):
    __tablename__ = "recipients_recipient"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    address_line = Column(String(500), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="Россия")
    note = Column(String(255))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="recipients")
    subscriptions = relationship("SubscriptionRecipient", back_populates="recipient")
    mailings = relationship("Mailing", back_populates="recipient")


class SubscriptionRecipient(Base):
    __tablename__ = "subscriptions_subscription_recipient"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions_subscription.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients_recipient.id"), nullable=False)
    emails_per_period = Column(Integer, default=1)

    # Relationships
    subscription = relationship("Subscription", back_populates="recipients")
    recipient = relationship("Recipient", back_populates="subscriptions")


class Post(Base):
    __tablename__ = "content_post"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources_source.id"), nullable=False)
    external_id = Column(String(255), index=True)
    media_type = Column(String(50))  # image, video, etc.
    media_url = Column(String(1024))
    thumbnail_url = Column(String(1024))
    caption = Column(Text)
    permalink = Column(String(1024))
    posted_at = Column(DateTime(timezone=True))
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(PostStatus), default=PostStatus.PENDING_REVIEW)

    # Relationships
    source = relationship("Source", back_populates="posts")
    mailing_items = relationship("MailingItem", back_populates="post")


class Template(Base):
    __tablename__ = "templates_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    preview_image = Column(String(255))
    config = Column(JSONB)  # Template configuration


class Mailing(Base):
    __tablename__ = "mailings_mailing"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions_subscription.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients_recipient.id"), nullable=False)
    scheduled_date = Column(DateTime(timezone=True))
    status = Column(Enum(MailingStatus), default=MailingStatus.PENDING)
    tracking_number = Column(String(100))
    label_url = Column(String(1024))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    subscription = relationship("Subscription", back_populates="mailings")
    recipient = relationship("Recipient", back_populates="mailings")
    items = relationship("MailingItem", back_populates="mailing")


class MailingItem(Base):
    __tablename__ = "mailings_mailingitem"

    id = Column(Integer, primary_key=True, index=True)
    mailing_id = Column(Integer, ForeignKey("mailings_mailing.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("content_post.id"), nullable=False)
    ordering = Column(Integer, default=0)
    template_id = Column(Integer, ForeignKey("templates_template.id"))
    generated_mockup_key = Column(String(500))  # Path to file or S3 key

    # Relationships
    mailing = relationship("Mailing", back_populates="items")
    post = relationship("Post", back_populates="mailing_items")
    template = relationship("Template")


class Payment(Base):
    __tablename__ = "billing_payment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions_subscription.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="RUB")
    status = Column(String(50), default="pending")
    yookassa_payment_id = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")
