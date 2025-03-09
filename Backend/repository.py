from sqlalchemy import select
from typing import List
from db import new_session, JobsdataTable, JobsnameTable
from models import JobAdd, JobSchema
from parser import get_vacancies  

class JobRepository:
    @classmethod
    async def add_one(cls, job_data: JobAdd) -> List[int]:
        vacancies = get_vacancies(job_data.name)
        if not vacancies:
            print("Нет вакансий, соответствующих запросу.")
            return []

        job_ids = []
        async with new_session() as session:
            for vacancy in vacancies:
                vacancy_name = vacancy.get('name')
                if not vacancy_name:
                    print("У вакансии отсутствует название.")
                    continue
                job_id = await cls._save_vacancy(session, vacancy)
                job_ids.append(job_id)

        return job_ids
    @staticmethod
    async def _save_vacancy(session, vacancy: dict) -> int:
        new_vacancy = JobsnameTable(name=vacancy['name'])
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
        return new_vacancy_data.job_id

    @classmethod
    async def find_all(cls) -> List[JobSchema]:
        async with new_session() as session:
            jobs= await cls._fetch_all_jobs(session)
            results_data = []
            for job in jobs:
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
    
    @staticmethod
    async def _fetch_all_jobs(session) -> List[JobsnameTable]:
        query = select(JobsnameTable).join(JobsdataTable, JobsnameTable.id == JobsdataTable.job_id)
        result = await session.execute(query)
        return result.scalars().all()