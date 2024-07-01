import requests

def get_vacancies(name:str):
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
                list_vacancies.append(title)
    else:
        print(f"Ошибка: {response.status_code}")
    return list_vacancies


