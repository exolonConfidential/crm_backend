from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="Property CRM Graph API",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")
