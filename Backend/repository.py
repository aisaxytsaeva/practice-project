from sqlalchemy import select
from typing import List, Optional
import aiohttp
from db import new_session, JobsdataTable, JobsnameTable
from models import JobAdd, JobSchema

class JobRepository:
    @classmethod
    async def add_one(cls, job_data: JobAdd) -> List[int]:
        async with new_session() as session:
            # Выполняем новый запрос к API hh.ru
            search_params = {'text': job_data.name}
            async with aiohttp.ClientSession() as http_session:
                async with http_session.get("https://api.hh.ru/vacancies", params=search_params) as response:
                    if response.status == 200:
                        data = await response.json()
                        all_vacancies = data['items']
                        if not all_vacancies:
                            print("Нет вакансий, соответствующих запросу.")
                            return []
                        filtered_vacancies = [
                            vacancy for vacancy in all_vacancies
                            if job_data.name.lower() in vacancy['name'].lower()
                        ]

                        if not filtered_vacancies:
                            print("Нет подходящих вакансий.")
                            return []

                        job_ids = []
                        for vacancy in filtered_vacancies:
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
                                sch=vacancy['schedule']['name'],
                                emp=vacancy['employment']['name'],
                                exp=vacancy['experience']['name']
                            )
                            session.add(new_vacancy_data)
                            await session.commit()

                            job_ids.append(new_vacancy_data.job_id)

                        return job_ids
                    else:
                        print(f"Ошибка: {response.status}")
                        return []

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