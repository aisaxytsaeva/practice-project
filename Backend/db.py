from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker





engine = create_async_engine(
    "sqlite+aiosqlite:///jobs.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class JobsnameTable(Model):
    __tablename__ = 'jobs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
       
class JobsdataTable(Model):
    __tablename__ = 'jobs_data'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id'))
    sch: Mapped[str]
    emp: Mapped[str]
    exp: Mapped[str]
    
    

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
