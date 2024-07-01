from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import JobAdd, JobSchema
from app.db import Model,  new_session, engine, JobsTable
from app.parser import get_vacancies


def get_db():
    db = new_session()
    try:
        yield db
    finally:

        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

Model.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/vacancy",
)





@router.post("/")
async def add_one(cls, job: JobAdd, db: db_dependency):
            
    jobs = db.query(JobsTable).all()
    list_jobs = get_vacancies(name = job.name)
    print(list_jobs)
    db_jobs = []
    for job in list_jobs:
        db_job = JobsTable(name=job['name'], sch=job['sch'], emp=job['emp'], exp=job['exp'])
        if db_job not in jobs:
            db.add(db_job)
            db.commit()
            db_jobs.append(db_job)
            db.refresh(db_job)
    return db_jobs


        

@router.get("/", response_model=List[JobSchema])
async def get_jobs(db: db_dependency):
    jobs = db.query(JobsTable).all()
    return jobs

@router.delete('/', response_model=List[JobSchema])
async def delete_vacancies(db: db_dependency):
    jobs = db.query(JobsTable).all()
    for job in jobs:
        db.delete(job)
        db.commit()
    return jobs