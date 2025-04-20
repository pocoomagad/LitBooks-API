from db.config import DATABASE_URL_asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

async_engine = create_async_engine(url=DATABASE_URL_asyncpg, echo=True)

conn = async_sessionmaker(async_engine, expire_on_commit=False)

