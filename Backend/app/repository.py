from sqlalchemy import select
import requests
from typing import List
from app.db import new_session, JobsTable
from app.models import JobAdd, JobSchema

class JobRepository:
    @classmethod
    async def add_one(cls, job_data: JobAdd ):
        async with new_session() as session:
            response = requests.get("https://api.hh.ru/vacancies", params={"name": job_data.model_dump()})
   
            vacancies = response.json()['items']
            for vacancy_id in vacancies:
                vac_id = vacancy_id['id']
            
            for vacancy in vacancies:
                vacancy_name = vacancy['name']

            
            for schedule in vacancies:
                schedule_name = schedule['schedule']['name']
 
            for employment in vacancies:
                employment_name = employment['employment']['name']

            for experience in vacancies:
                experience_name = experience['experience']['name']

            job = JobsTable(id=vac_id, name=vacancy_name, sch=schedule_name, emp=employment_name, exp=experience_name)
            
            session.add(job)
            await session.flush()
            await session.commit()
            return job.id
    @classmethod
    async def find_all(cls) -> List[JobSchema]:
        async with new_session() as session:
            query = select(JobsTable)
            result = await session.execute(query)
            job_models = result.scalars().all()
            job_schemas = [JobSchema.model_validate(job_model) for job_model in job_models]
            return job_schemas