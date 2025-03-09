from typing import List
import requests

def get_vacancies(job_name: str) -> List[dict]:
    search_params = {'text': job_name}
    response = requests.get("https://api.hh.ru/vacancies", params=search_params)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return []

    vacancies = response.json()['items']
    return [
        {
            'name': vacancy['name'],
            'schedule': vacancy['schedule']['name'],
            'employment': vacancy['employment']['name'],
            'experience': vacancy['experience']['name']
        }
        for vacancy in vacancies
        if job_name.lower() in vacancy['name'].lower()
    ]


