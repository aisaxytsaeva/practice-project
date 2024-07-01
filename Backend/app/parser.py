import requests

def get_vacancies(name:str):
    search_params = {
        'profession': name,
    }
    list_vacancies = []
    response = requests.get("https://api.hh.ru/vacancies",search_params)

            
    if response.status_code == 200:
        vacancies = response.json()['items']
        found_match = False
        for vacancy in vacancies:
            if any(word in vacancy['name'].split() for word in name):
                found_match = True
                break
            if not found_match:
                pass
            if found_match == True:
                for vacancy in vacancies:
                    vacancy_name = {vacancy['name']}
                    schedule_name = {vacancy['schedule']['name']}
                    employment_name = {vacancy['employment']['name']}
                    experience_name = {vacancy['experience']['name']}
                    data = {
                        'name': vacancy_name,
                        'schedule': schedule_name,
                        'employment': employment_name,
                        'experience': experience_name
                    }
                    list_vacancies.append(data)
    else:
        print(f"Ошибка: {response.status_code}")
    return list_vacancies

print(get_vacancies('Менеджер'))