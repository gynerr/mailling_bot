import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, DeclarativeBase

load_dotenv()
meta = MetaData()

# Initialize declarative base with metadata
Base: DeclarativeBase = declarative_base(metadata=meta)

engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
    echo=True
)


async def setup_database() -> None:
    async with engine.connect() as conn:
        await conn.run_sync(meta.reflect)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
