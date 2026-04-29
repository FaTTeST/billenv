"""
Главное приложение FastAPI для PostSocial.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine, Base
from app.api import api_router

# Создание таблиц базы данных (для разработки)
# В продакшене использовать Alembic миграции
Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    """Создать и настроить приложение FastAPI."""
    
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Сервис автоматической доставки цифрового контента почтой",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    
    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Настроить для продакшена
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Подключение роутов
    application.include_router(api_router, prefix="/api")
    
    @application.get("/")
    def root():
        """Корневой эндпоинт."""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running"
        }
    
    @application.get("/health")
    def health_check():
        """Проверка здоровья приложения."""
        return {"status": "healthy"}
    
    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
