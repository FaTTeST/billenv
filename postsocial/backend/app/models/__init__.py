"""
Инициализация модуля models.
"""
from app.models.models import (
    User,
    Plan,
    Subscription,
    Source,
    Recipient,
    SubscriptionRecipient,
    Post,
    Template,
    Mailing,
    MailingItem,
    Payment,
    SourceType,
    SubscriptionStatus,
    PostStatus,
    MailingStatus,
    PaymentStatus,
)

__all__ = [
    "User",
    "Plan",
    "Subscription",
    "Source",
    "Recipient",
    "SubscriptionRecipient",
    "Post",
    "Template",
    "Mailing",
    "MailingItem",
    "Payment",
    "SourceType",
    "SubscriptionStatus",
    "PostStatus",
    "MailingStatus",
    "PaymentStatus",
]
