from typing import Annotated, List
from fastapi import APIRouter, Depends
from app.models import JobAdd, JobSchema, JobId
from app.repository import JobRepository
from app.db import new_session, JobsdataTable, JobsnameTable
import requests


router = APIRouter(
    prefix="/vacancy",
)





@router.post("/")
async def add_one(cls, job_data: JobAdd ):
    async with new_session() as session:
        search_params = job_data.model_dump()
        filtered_vacancies = []
        response = requests.get("https://api.hh.ru/vacancies", params=search_params) 
        if response.status_code == 200:
            all_vacancies = response.json()['items']
            filtered_vacancies = []
            for vacancy in all_vacancies:
                vacancy_name = vacancy['name']
                schedule_name = vacancy['schedule']['name']
                employment_name = vacancy['employment']['name']
                experience_name = vacancy['experience']['name']
                if (search_params['name'].lower() in vacancy['name'].lower()):
                    new_vacancy = JobsnameTable(name=vacancy_name)
                    session.add(new_vacancy)
                    await session.commit()
                    new_vacancy_data = JobsdataTable(
                        job_id=new_vacancy.id,
                        sch= schedule_name,
                        emp = employment_name,
                        exp=experience_name
                    )
                    session.add(new_vacancy_data)
                    await session.commit()
                        
                    filtered_vacancies.append({
                        'name': vacancy_name,
                        'schedule': schedule_name,
                        'employment': employment_name,
                        'experience': experience_name
                    })
                    return new_vacancy_data.job_id
                        
                else:
                    title='Простите, ничего не нашлось :('
                    print(title)
                    return None
        else:
            print(f"Ошибка: {response.status_code}")

@router.get("/")
async def get_jobs() -> List[JobSchema]:
    jobs = await JobRepository.find_all()
    jobs_schema = list(map(lambda job: JobSchema(**job.dict()), jobs)) 
    return jobs_schema
