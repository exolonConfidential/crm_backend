from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.database import engine


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)


async def get_async_session():
    """
    Provides a request-scoped AsyncSession.

    - Starts implicit transaction on first DB operation
    - Commits if request succeeds
    - Rolls back if any exception occurs
    - Prevents nested transaction errors
    - Prevents connection leaks
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise