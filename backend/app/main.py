from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=f"{settings.API_V1_STRING}/docs",
    redoc_url=f"{settings.API_V1_STRING}/redoc",
    openapi_url=f"{settings.API_V1_STRING}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STRING)
