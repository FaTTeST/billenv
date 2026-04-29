"""
Модуль безопасности: аутентификация, авторизация, хеширование.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from app.core.config import settings


# Хеширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хешировать пароль."""
    return pwd_context.hash(password)


# JWT токены
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создать JWT токен доступа."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Декодировать JWT токен."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


# Шифрование токенов соцсетей (Fernet)
def get_fernet() -> Fernet:
    """Получить Fernet шифратор."""
    if not settings.FERNET_KEY:
        # Генерируем новый ключ для разработки
        return Fernet(Fernet.generate_key())
    return Fernet(settings.FERNET_KEY.encode())


def encrypt_token(token: str) -> str:
    """Зашифровать токен."""
    fernet = get_fernet()
    return fernet.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Расшифровать токен."""
    fernet = get_fernet()
    return fernet.decrypt(encrypted_token.encode()).decode()
