from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.property import Property


class PropertyRepository:
    @staticmethod
    async def get_by_location_id(session, location_id: int):

        stmt = (
            select(Property)
            .options(
                selectinload(Property.owner),
                selectinload(Property.location),
            )
            .where(Property.location_id == location_id)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()