from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from ..settings import settings

_engine = create_async_engine(
    settings.database_url
)

Session = sessionmaker(
    _engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncSession:
    session = Session()
    try:
        yield session
    finally:
        await session.close()
