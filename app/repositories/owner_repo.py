from sqlalchemy import select
from db.models.owner import Owner

class OwnerRepository:

    @staticmethod
    async def update(session, owner, data: dict):
        for key, value in data.items():
            setattr(owner, key, value)
        await session.flush()
        return owner
    
    @staticmethod
    async def get_by_phone(session, phone: str):
        return await session.scalar(select(Owner).where(Owner.phone_number == phone))
    
    @staticmethod
    async def get_by_email(session, email: str):
        return await session.scalar(select(Owner).where(Owner.email == email))