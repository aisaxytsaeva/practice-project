from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped




engine = create_async_engine(
    "sqlite+aiosqlite:///jobs.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class JobsTable(Model):
    __tablename__ = 'jobs'
    
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    sch: Mapped[str]
    exp: Mapped[str]
    emp: Mapped[str]

    
    

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)