from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_collumn




engine = create_async_engine(
    "sqlite+aiosqlite:///jobs.db"
)

nem_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class JobsTable(Model):
    __tablename__ = 'jobs'
    
    id: Mapped[int] = mapped_collumn(primary_key=True)
    name: Mapped[str]
    area: Mapped[str]
    schelude: Mapped[str]
    exp: Mapped[str]
    emp: Mapped[str]

    
    

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)