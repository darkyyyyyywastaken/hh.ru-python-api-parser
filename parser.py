import requests
import ctypes
import pandas as pd
from datetime import datetime

## attention pls
## this code forced to searching by company id,
## where in url (employer_id=1) needs to be your custom id(read hh api info or seek on your own)
## or put in -url- YOUR api request
## also, i forgot to put in the end error and stop code, when request gets a timeout

url = f"https://api.hh.ru/vacancies?from=employerPage&employer_id=1&per_page=100"

response = requests.get(url)
data = response.json()

vacancies = []
for item in data['items']:
    vacancy_title = item['name']
    city = item['area']['name'] if item['area'] else "Не указан"
    salary_from = item['salary']['from'] if item['salary'] else "Не указана"
    salary_to = item['salary']['to'] if item['salary'] else "Не указана"
    vacancy_link = item['alternate_url']

    vacancies.append({
        'Вакансия': vacancy_title,
        'Город': city,
        'Зарплата от': salary_from,
        'Зарплата до': salary_to,
        'Ссылка': f'<a href="{vacancy_link}" target="_blank">Просмотр вакансии</a>'
    })

df = pd.DataFrame(vacancies)
html_table = df.to_html(index=False, escape=False)
date_str = datetime.now().strftime("%d-%m-%Y")
html_content = f"<html><head><title>Вакансии</title></head><body><h1>Вакансии на {date_str}</h1>{html_table}</body></html>"
file_name = f"Вакансии_{date_str}.html"
with open(f"Вакансии_{date_str}.html", "w", encoding="utf-8") as file:
        file.write(html_content)

ctypes.windll.user32.MessageBoxW(0, f"HTML-таблица создана и сохранена в файле '{file_name}'.", "Генерация списка вакансий", 0)