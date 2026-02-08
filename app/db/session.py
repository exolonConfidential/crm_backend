from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.database import engine

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
