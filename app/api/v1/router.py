from fastapi import APIRouter
from app.api.v1.property_routes import router as property_routes

api_router = APIRouter()
api_router.include_router(property_routes)
