from fastapi import APIRouter
from app.api.v1.endpoints.map import router as map_routes
from app.api.v1.endpoints.property import router as property_routes

api_router = APIRouter()
api_router.include_router(map_routes)
api_router.include_router(property_routes)
