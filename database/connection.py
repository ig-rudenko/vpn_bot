from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .base import Base


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None

    def init(self, dsn: str):
        self._engine = create_async_engine(dsn)
        self._session = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await self._engine.dispose()


db = AsyncDatabaseSession()
