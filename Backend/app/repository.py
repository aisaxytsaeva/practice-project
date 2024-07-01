from sqlalchemy import select
import requests
from app.db import new_session, JobsdataTable, JobsnameTable
from app.models import JobAdd, JobSchema


class JobRepository: 
    @classmethod
    async def add_one(name, job_data: JobAdd ):
        async with new_session() as session:
            search_params = {
                'profession': name,
            }
            list_vacancies = []
            response = requests.get("https://api.hh.ru/vacancies", params=search_params) 
            if response.status_code == 200:
                all_vacancies = response.json()['items']
                for vacancy in all_vacancies:
                    if search_params['profession'].lower() in vacancy['name'].lower():
                        vacancy_name = vacancy['name']
                        schedule_name = vacancy['schedule']['name']
                        employment_name = vacancy['employment']['name']
                        experience_name = vacancy['experience']['name']
                        data = {
                            'name': vacancy_name,
                            'schedule': schedule_name,
                            'employment': employment_name,
                            'experience': experience_name
                        }
                        list_vacancies.append(data)
                    else:
                        title='Простите, ничего не нашлось :('
                        print(title)
            else:
                print(f"Ошибка: {response.status_code}")
                return list_vacancies
            
            
            session.add(job)
            await session.flush()
            await session.commit()

    @classmethod
    async def find_all(cls) -> List[JobSchema]:
        async with new_session() as session:
            query = select(JobsTable)
            result = await session.execute(query)
            job_models = result.scalars().all()
            job_schemas = [JobSchema(id=job_model.id, name=job_model.name, sch=job_model.sch, emp=job_model.emp, exp=job_model.exp) for job_model in job_models]
            return job_schemas
