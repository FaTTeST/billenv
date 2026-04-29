# FastAPI application factory
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .db.session import engine, Base
from .api import auth, users, subscriptions, sources, recipients, posts, mailings, plans, payments


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed
    pass


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Автоматизированный сервис офлайн-доставки цифрового контента",
        lifespan=lifespan
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Authentication"])
    app.include_router(users.router, prefix=f"{settings.API_PREFIX}/users", tags=["Users"])
    app.include_router(plans.router, prefix=f"{settings.API_PREFIX}/plans", tags=["Plans"])
    app.include_router(subscriptions.router, prefix=f"{settings.API_PREFIX}/subscriptions", tags=["Subscriptions"])
    app.include_router(sources.router, prefix=f"{settings.API_PREFIX}/sources", tags=["Sources"])
    app.include_router(recipients.router, prefix=f"{settings.API_PREFIX}/recipients", tags=["Recipients"])
    app.include_router(posts.router, prefix=f"{settings.API_PREFIX}/posts", tags=["Posts"])
    app.include_router(mailings.router, prefix=f"{settings.API_PREFIX}/mailings", tags=["Mailings"])
    app.include_router(payments.router, prefix=f"{settings.API_PREFIX}/payments", tags=["Payments"])

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "Ваша лента продолжает жить — там, где интернет заканчивается."
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()
