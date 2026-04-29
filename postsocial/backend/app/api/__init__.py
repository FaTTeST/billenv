"""
Инициализация модуля api.
"""
from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.recipients import router as recipients_router

# Создаем главный роутер API
api_router = APIRouter()

# Подключаем роуты
api_router.include_router(auth_router)
api_router.include_router(recipients_router)

__all__ = ["api_router"]
