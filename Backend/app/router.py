from fastapi import APIRouter
from sqlalchemy import select
import requests
from db import new_session, JobsTable
from models import JobAdd, JobSchema



router = APIRouter(
    prefix="/vacancy",
)


@router.post("/")
async def add_one(cls, job_data: JobAdd ):
    async with new_session() as session:
        response = requests.get('https://api.hh.ru/vacancies')
        data = response.json()
        job_dict = job_data.model_dump()
        job = JobsTable(**job_dict)
        
        session.add(job)
        await session.flush()
        await session.commit()
        return job.id
        

@router.get("/")
async def find_all(cls) -> list[JobSchema]:
    async with new_session() as session:
        query = select(JobsTable)
        result = await session.execute(query)
        job_models = result.scalars().all()
        job_schemas = [JobSchema.model_validate(job_model) for job_model in job_models]
        return job_schemas