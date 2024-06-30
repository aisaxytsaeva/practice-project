from sqlalchemy import select
from typing import List


from pydantic import BaseModel


class JobAdd(BaseModel):
    name: str
    
    
class JobSchema(BaseModel):
    id: int
    name: str
    sch: str
    emp: str
    exp: str


class JobId(BaseModel):
    ok: bool= True
    job_id: int
    
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



   
class JobRepository:   
    @classmethod
    async def find_all(cls) -> List[JobSchema]:
        async with new_session() as session:
            query = select(JobsTable)
            result = await session.execute(query)
            job_models = result.scalars().all()
            job_schemas = [JobSchema.model_validate(job_model) for job_model in job_models]
            return job_schemas
        
        
from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.models import JobAdd, JobId, JobSchema
from app.repository import JobRepository


router = APIRouter(
    prefix="/vacancy",
)

@router.get("/")
async def get_jobs() -> List[JobSchema]:
    jobs= await JobRepository.find_all()
    return jobs
