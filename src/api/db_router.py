from db.engines import async_engine
from fastapi import APIRouter
from model.basic import Base

db_rout = APIRouter(prefix="/db")


@db_rout.post("", tags=["DB"])
async def setup():
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)