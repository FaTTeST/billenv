"""
SQLAlchemy модели базы данных PostSocial.
"""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, 
    Text, Float, JSON, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


# === ENUMS ===
class SourceType(str, PyEnum):
    """Типы источников контента."""
    INSTAGRAM = "instagram"
    VK = "vk"
    TELEGRAM = "telegram"
    MANUAL = "manual"


class SubscriptionStatus(str, PyEnum):
    """Статусы подписки."""
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PostStatus(str, PyEnum):
    """Статусы постов."""
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    USED = "used"


class MailingStatus(str, PyEnum):
    """Статусы рассылок."""
    PENDING = "pending"
    PRINTED = "printed"
    SENT = "sent"
    RETURNED = "returned"


class PaymentStatus(str, PyEnum):
    """Статусы платежей."""
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


# === МОДЕЛИ ===

class User(Base):
    """Пользователь сервиса."""
    __tablename__ = "users_user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_operator = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    
    # Связи
    sources = relationship("Source", back_populates="user", cascade="all, delete-orphan")
    recipients = relationship("Recipient", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Plan(Base):
    """Тарифный план."""
    __tablename__ = "plans_plan"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    price_per_month = Column(Float, nullable=False)
    mailing_count_per_month = Column(Integer, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    """Подписка пользователя."""
    __tablename__ = "subscriptions_subscription"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans_plan.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, nullable=False)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    payment_method_id = Column(String(255))
    is_auto_renew = Column(Boolean, default=True)
    cancelled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    recipients = relationship("SubscriptionRecipient", back_populates="subscription", cascade="all, delete-orphan")
    mailings = relationship("Mailing", back_populates="subscription", cascade="all, delete-orphan")


class Source(Base):
    """Источник контента (соцсеть)."""
    __tablename__ = "sources_source"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)
    external_id = Column(String(255))  # ID аккаунта в соцсети
    access_token = Column(Text)  # Зашифрованный токен
    refresh_token = Column(Text)  # Зашифрованный refresh token
    token_expires = Column(DateTime)
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime)
    extra_data = Column(JSONB)  # Дополнительные данные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="sources")
    posts = relationship("Post", back_populates="source", cascade="all, delete-orphan")


class Recipient(Base):
    """Получатель писем."""
    __tablename__ = "recipients_recipient"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    address_line = Column(Text, nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="Россия")
    note = Column(String(255))  # Примечание (например, "бабушка Нина")
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="recipients")
    subscriptions = relationship("SubscriptionRecipient", back_populates="recipient", cascade="all, delete-orphan")


class SubscriptionRecipient(Base):
    """Связь подписки и получателя с настройками."""
    __tablename__ = "subscriptions_subscription_recipient"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions_subscription.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients_recipient.id"), nullable=False)
    emails_per_period = Column(Integer, default=1)  # Количество писем в период
    
    __table_args__ = (
        UniqueConstraint('subscription_id', 'recipient_id', name='unique_subscription_recipient'),
    )
    
    # Связи
    subscription = relationship("Subscription", back_populates="recipients")
    recipient = relationship("Recipient", back_populates="subscriptions")
    mailings = relationship("Mailing", back_populates="recipient")


class Post(Base):
    """Пост из социальной сети."""
    __tablename__ = "content_post"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources_source.id"), nullable=False)
    external_id = Column(String(255), index=True)  # ID поста в соцсети
    media_type = Column(String(50))  # image, video, album
    media_url = Column(Text)  # URL изображения
    thumbnail_url = Column(Text)  # URL превью
    caption = Column(Text)  # Текст поста
    permalink = Column(Text)  # Ссылка на пост
    posted_at = Column(DateTime)  # Дата публикации в соцсети
    collected_at = Column(DateTime, default=datetime.utcnow)  # Дата сбора сервисом
    status = Column(Enum(PostStatus), default=PostStatus.PENDING_REVIEW)
    
    # Связи
    source = relationship("Source", back_populates="posts")
    mailing_items = relationship("MailingItem", back_populates="post")


class Template(Base):
    """Шаблон оформления письма."""
    __tablename__ = "templates_template"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    preview_image = Column(Text)  # URL превью шаблона
    config = Column(JSONB)  # Конфигурация шаблона
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Mailing(Base):
    """Рассылка (почтовое отправление)."""
    __tablename__ = "mailings_mailing"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions_subscription.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients_recipient.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)  # Планируемая дата отправки
    status = Column(Enum(MailingStatus), default=MailingStatus.PENDING)
    tracking_number = Column(String(100))  # Трек-номер
    label_url = Column(Text)  # URL этикетки/макета
    sent_at = Column(DateTime)  # Фактическая дата отправки
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    subscription = relationship("Subscription", back_populates="mailings")
    recipient = relationship("SubscriptionRecipient", back_populates="mailings")
    items = relationship("MailingItem", back_populates="mailing", cascade="all, delete-orphan")


class MailingItem(Base):
    """Элемент рассылки (конкретный пост в письме)."""
    __tablename__ = "mailings_mailingitem"
    
    id = Column(Integer, primary_key=True, index=True)
    mailing_id = Column(Integer, ForeignKey("mailings_mailing.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("content_post.id"), nullable=False)
    ordering = Column(Integer, default=0)  # Порядок в письме
    template_id = Column(Integer, ForeignKey("templates_template.id"))
    generated_mockup_key = Column(Text)  # Путь к файлу макета
    
    # Связи
    mailing = relationship("Mailing", back_populates="items")
    post = relationship("Post", back_populates="mailing_items")
    template = relationship("Template")


class Payment(Base):
    """Платёж."""
    __tablename__ = "billing_payment"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_user.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions_subscription.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="RUB")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    yookassa_payment_id = Column(String(255), index=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    
    # Связи
    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription")
