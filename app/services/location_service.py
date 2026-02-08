from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.location_repo import LocationRepository


class LocationService:

    @staticmethod
    async def get_nearby_locations(session: AsyncSession, lat: float, lon: float, radius: int = 2000):
        return await LocationRepository.find_within_radius(
            session=session,
            lat=lat,
            lon=lon,
            radius_m=radius
        )