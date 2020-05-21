import re
import requests
from bs4 import BeautifulSoup as BS
import json

i = 0
x = 0
database_faq = {}


for num_link in range(170, 321):
    link = f'https://www.minobrnauki.gov.ru/ru/activity/other/info_koronavirus/questions_answers/?id_4={num_link}'
    req = requests.get(link)

    if req.status_code == 200:
        i += 1
        # print(i)
        page = req.text
        soup = BS(page, "html.parser")

        # Поиск вопросов
        question = soup.find_all("h1")
        question = str(question[1])
        question = re.sub("[</h1>]+", "", question)
        # print(question)

        # Поиск ответов
        answer = soup.get_text()
        answer = re.findall('\d\d\.\d\d\.\d\d\d\d\n\n\n[^\']+О министерстве', answer)
        answer = str(answer[0])
        answer = re.sub("[\n\r]+", " ", answer)
        answer = re.sub("^\d\d\.\d\d\.\d\d\d\d", "", answer)
        answer = re.sub("^[\s]+", "", answer)
        answer = re.sub("О министерстве$", "", answer)
        # print(answer)

        database_faq[question] = answer

    else:
        print(f'Что-то пошло не так на странице: {link}')
        x += 1
        
# print(database_faq)

with open('file_base', 'w', encoding='utf-8') as file:
    json_base = json.dump(database_faq, file)


print(f"OK! Обработано {i} страниц. Нет контента на {x} страницах")
