from sqlalchemy import select
from typing import List
from db import new_session, JobsdataTable, JobsnameTable
from models import JobAdd, JobSchema
from parser import get_vacancies  

class JobRepository:
    @classmethod
    async def add_one(cls, job_data: JobAdd) -> List[int]:
        async with new_session() as session:

            list_vacancies = get_vacancies(job_data.name)
            
            if not list_vacancies:
                print("Нет вакансий, соответствующих запросу.")
                return []

            job_ids = []
            for vacancy in list_vacancies:
                if isinstance(vacancy, dict):  
                    vacancy_name = vacancy['name']
                    existing_job = await session.execute(select(JobsnameTable).where(JobsnameTable.name == vacancy_name))
                    if existing_job.scalars().first():
                        print(f"Вакансия '{vacancy_name}' уже существует в базе данных.")
                        continue
                    
                    new_vacancy = JobsnameTable(name=vacancy_name)
                    session.add(new_vacancy)
                    await session.commit()

                    new_vacancy_data = JobsdataTable(
                        job_id=new_vacancy.id,
                        sch=vacancy['schedule'],
                        emp=vacancy['employment'],
                        exp=vacancy['experience']
                    )
                    session.add(new_vacancy_data)
                    await session.commit()

                    job_ids.append(new_vacancy_data.job_id)

            return job_ids

    @classmethod
    async def find_all(cls) -> List[JobSchema]:
        async with new_session() as session:
            query = select(JobsnameTable).join(JobsdataTable, JobsnameTable.id == JobsdataTable.job_id)
            result = await session.execute(query)
            job_models = result.scalars().all()
            results_data = []
            for job in job_models:
                job_data = await session.execute(select(JobsdataTable).where(JobsdataTable.job_id == job.id))
                job_data = job_data.scalars().first()
                if job_data:
                    results_data.append(JobSchema(
                        id=job.id,
                        name=job.name,
                        sch=job_data.sch,
                        emp=job_data.emp,
                        exp=job_data.exp
                    ))
            return results_data