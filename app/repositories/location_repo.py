from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.location import Location
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from geoalchemy2.functions import ST_DWithin


class LocationRepository:

    @staticmethod
    async def get_by_osm(session: AsyncSession, osm_type: str, osm_id: int):
        stmt = select(Location).where(
            Location.osm_type == osm_type,
            Location.osm_id == osm_id
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


    @staticmethod
    async def create(session, data):
        # For geography this is still correct
        geom = from_shape(Point(data["longitude"], data["latitude"]), srid=4326)

        location = Location(
            **data,
            geom=geom
        )

        session.add(location)
        await session.flush()
        return location
    

    @staticmethod
    async def find_within_radius(session, lat, lon, radius_m=2000):
        # Create a geography point instead of string
        point = from_shape(Point(lon, lat), srid=4326)

        stmt = select(Location).where(
            ST_DWithin(
                Location.geom,
                point,
                radius_m
            )
        )

        result = await session.execute(stmt)
        return result.scalars().all()