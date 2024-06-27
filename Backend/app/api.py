import requests
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Database is clear")
    await create_tables()
    print("Database is ready")
    yield
    print("Turning off")


response = requests.get('https://api.hh.ru/vacancies')

vacancy_list = [] 
vacancies = response.json()['items']
for vacancy in vacancies:
    name = vacancy['name']
    print(f"Вакансия: {name}")
    vacancy_list.append(name)
