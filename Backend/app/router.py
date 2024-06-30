from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.models import JobAdd, JobId, JobSchema
from app.repository import JobRepository


router = APIRouter(
    prefix="/vacancy",
)


@router.post("/")
async def add_job(
    job: Annotated[JobAdd, Depends()],
)-> JobId:
    job_id = await JobRepository.add_one(job)
    return JobId(ok=True, job_id=job_id)

        

@router.get("/")
async def get_jobs() -> List[JobSchema]:
    jobs= await JobRepository.find_all()
    return jobs
