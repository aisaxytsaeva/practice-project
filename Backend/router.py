from typing import List
from fastapi import APIRouter
from db import create_tables, delete_tables
from models import JobAdd, JobSchema
from repository import JobRepository

router = APIRouter(prefix="/vacancy")

@router.get("/")
async def get_jobs(profession: str) -> List[JobSchema]:
    await delete_tables()
    await create_tables()
    job_data = JobAdd(name=profession)  
    job_ids = await JobRepository.add_one(job_data)
    if job_ids:
        jobs = await JobRepository.find_all()
        return jobs
    else:
        return []