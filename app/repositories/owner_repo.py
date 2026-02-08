class OwnerRepository:

    @staticmethod
    async def update(session, owner, data: dict):
        for key, value in data.items():
            setattr(owner, key, value)
        await session.flush()
        return owner