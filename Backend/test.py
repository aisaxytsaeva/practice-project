# from sqlalchemy import select
# from typing import List
# import requests


# from pydantic import BaseModel


# class JobAdd(BaseModel):
#     name: str
    
    
# class JobSchema(BaseModel):
#     id: int
#     name: str
#     sch: str
#     emp: str
#     exp: str


# class JobId(BaseModel):
#     ok: bool= True
#     job_id: int
    
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped




# engine = create_async_engine(
#     "sqlite+aiosqlite:///jobs.db"
# )

# new_session = async_sessionmaker(engine, expire_on_commit=False)

# class Model(DeclarativeBase):
#     pass


# class JobsTable(Model):
#     __tablename__ = 'jobs'
    
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     sch: Mapped[str]
#     exp: Mapped[str]
#     emp: Mapped[str]

    
    

# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)

# async def delete_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.drop_all)



   
# class JobRepository: 
#     @classmethod
#     async def add_one(name, job_data: JobAdd ):
#         async with new_session() as session:
#             search_params = {
#                 'profession': name,
#             }
#             list_vacancies = []
#             response = requests.get("https://api.hh.ru/vacancies", params=search_params) 
#             if response.status_code == 200:
#                 all_vacancies = response.json()['items']
#                 for vacancy in all_vacancies:
#                     if search_params['profession'].lower() in vacancy['name'].lower():
#                         vacancy_name = vacancy['name']
#                         schedule_name = vacancy['schedule']['name']
#                         employment_name = vacancy['employment']['name']
#                         experience_name = vacancy['experience']['name']
#                         data = {
#                             'name': vacancy_name,
#                             'schedule': schedule_name,
#                             'employment': employment_name,
#                             'experience': experience_name
#                         }
#                         list_vacancies.append(data)
#                     else:
#                         title='Простите, ничего не нашлось :('
#                         print(title)
#             else:
#                 print(f"Ошибка: {response.status_code}")
#                 return list_vacancies
            


#     @classmethod
#     async def find_all(cls) -> List[JobSchema]:
#         async with new_session() as session:
#             query = select(JobsTable)
#             result = await session.execute(query)
#             job_models = result.scalars().all()
#             job_schemas = [JobSchema(id=job_model.id, name=job_model.name, sch=job_model.sch, emp=job_model.emp, exp=job_model.exp) for job_model in job_models]
#             return job_schemas

        
# from typing import Annotated, List
# from fastapi import APIRouter, Depends
# from app.models import JobAdd, JobId, JobSchema
# from app.repository import JobRepository


# router = APIRouter(
#     prefix="/vacancy",
# )

# @router.post("/")
# async def add_job(
#     job: Annotated[JobAdd, Depends()],
# )-> JobId:
#     job_id = await JobRepository.add_one(job)
#     return JobId(ok=True, job_id=job_id)

        

# @router.get("/")
# async def get_jobs() -> List[JobSchema]:
#     jobs = await JobRepository.find_all()
#     jobs_schema = list(map(lambda job: JobSchema(**job.dict()), jobs)) 
#     return jobs_schema
