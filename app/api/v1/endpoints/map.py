from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.services.location_service import LocationService
from app.schemas.map_schema import MapQueryResponse

router = APIRouter(prefix="/map", tags=["Map"])


@router.get("/query", response_model=MapQueryResponse)
async def query_nearby_locations(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(2000, gt=0, le=50000),
    session: AsyncSession = Depends(get_async_session),
):
    """
        Returns all locations within a given radius from a lat/lon point.
        Uses PostGIS ST_DWithin (geography).
    """

    try:
        locations = await LocationService.get_nearby_locations(
            session=session,
            lat=lat,
            lon=lon,
            radius= radius
        )

        return MapQueryResponse(
            total=len(locations),
            locations=locations
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch nearby locations"
        )