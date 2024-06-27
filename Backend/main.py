import requests


response = requests.get('https://api.hh.ru/vacancies')

vacancies = response.json()['items']
for vacancy in vacancies:
    name = vacancy['name']
    print(f"Вакансия: {name}")