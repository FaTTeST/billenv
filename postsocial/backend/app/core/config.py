"""
Конфигурация приложения PostSocial.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Приложение
    APP_NAME: str = "PostSocial"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # База данных
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/postsocial"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Шифрование токенов соцсетей
    FERNET_KEY: Optional[str] = None
    
    # Файловое хранилище
    STORAGE_PATH: str = "./storage"
    
    # Интеграции
    YOOKASSA_SHOP_ID: Optional[str] = None
    YOOKASSA_SECRET_KEY: Optional[str] = None
    
    INSTAGRAM_APP_ID: Optional[str] = None
    INSTAGRAM_APP_SECRET: Optional[str] = None
    
    VK_APP_ID: Optional[str] = None
    VK_APP_SECRET: Optional[str] = None
    
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # Уведомления
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    CLOUD_RU_NOTIFICATIONS_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Получить кэшированные настройки."""
    return Settings()


settings = get_settings()
