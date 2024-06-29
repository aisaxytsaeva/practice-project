import requests
from app.models import JobSchema
response = requests.get('https://api.hh.ru/vacancies')



vacancies = response.json()['items']

for vacancy_id in vacancies:
    vac_id = vacancy_id['id']
    job = JobSchema(id=vac_id)

vacancies = response.json()['items']
for vacancy in vacancies:
     vacancy_name = vacancy['name']
     job = JobSchema( name=vacancy_name)
        
for salary in vacancies:
    if vacancy['salary']['from'] == None:
        salary_name = 'Зарплата не указана'
    else:
        salary_name = vacancy['salary']['from']
    
                
for area in vacancies:
    area_name = area['area']
  
            
for schedule in vacancies:
    schedule_name = schedule['schedule']['name']
    job = JobSchema(sch=schedule_name)
 
for employment in vacancies:
   employment_name = employment['employment']['name']
   job = JobSchema( emp=employment_name)

for experience in vacancies:
    experience_name = experience['experience']['name']
    job = JobSchema(exp=experience_name)

job = JobSchema(id=vac_id, name=vacancy_name, sch=schedule_name, emp=employment_name, exp=experience_name)
print(job)