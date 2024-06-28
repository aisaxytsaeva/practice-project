import requests
response = requests.get('https://api.hh.ru/vacancies')
data = response.json()


vacancies_list = []
vacancies = response.json()['items']
for vacancy in vacancies:
    title = vacancy['name']
    vacancies_list.append(title)
    print(vacancies_list)

area_list = []
for area in vacancies:
    title = area['area']
    area_list.append(title)

schedule_list = []
for scedule in vacancies:
    title = scedule['schedule']['name']
    schedule_list.append(title)
    print(schedule_list)
    

employment_list = []
for employment in vacancies:
    title = employment['employment']['name']
    employment_list.append(title)
    print(employment_list)

experience_list = []
for experience in vacancies:
    title = experience['experience']['name']
    experience_list.append(title)
    print(experience_list)