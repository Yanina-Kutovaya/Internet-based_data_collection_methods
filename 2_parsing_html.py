import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import re
import json
from pprint import pprint

# Необходимо собрать информацию о вакансиях на вводимую должность с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:

# - Наименование вакансии
# - Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
# - Ссылку на саму вакансию
# - Сайт откуда собрана вакансия

# Данная структура должна быть одинаковая для вакансий с обоих сайтов.

position = 'python'
hh_page_n = 2
superjob_page_n = 1

main_link_1 = 'https://hh.ru'
main_link_2 = 'https://russia.superjob.ru'


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/80.0.3987.149 Safari/537.36'}

params_1 = {'L_is_autosearch': False,
            'country': 1,
            'area': 113,
            'clusters': True,
            'enable_snippets': True,
            'text': position,
            'only_with_salary': False,
            'page': hh_page_n}

params_2 = {'keywords': position,
            'page': superjob_page_n}


response_1 = requests.get(f'{main_link_1}/search/vacancy', headers=headers, params=params_1).text
response_2 = requests.get(f'{main_link_2}/vacancy/search', headers=headers, params=params_2).text

soap = bs(response_1, 'lxml')
div = soap.find_all('div', {'class': "vacancy-serp-item__row vacancy-serp-item__row_header"})

soap_2 = bs(response_2, 'lxml')
div_2 = soap_2.find_all('div', {'class': "acdxh GPKTZ _1tH7S"})


df = {}
for i in range(len(div)):
    df[i] = {'name': div[i].findChildren()[4].text.replace('\xa0', ' '),
             'link': div[i].findChildren()[4].get('href'),
             'site': main_link_1,
             'min_salary': np.nan,
             'max_salary': np.nan,
             'currency': np.nan}

    salary = div[i].findChildren(recursive=False)[1].text
    if salary != '':
        df[i]['currency'] = salary[-4:].replace(' ', '')

        salary = salary.replace('\xa0', '').replace(' ', '')
        if salary[:2] == 'от':
            df[i]['min_salary'] = int(re.findall('от([\d]*)', salary)[0])
        elif salary[:2] == 'до':
            df[i]['max_salary'] = int(re.findall('до([\d]*)', salary)[0])
        elif re.findall('-', salary):
            df[i]['min_salary'] = int(re.findall('([\d]*)-', salary)[0])
            df[i]['max_salary'] = int(re.findall('-([\d]*)', salary)[0])

n = len(div)
for i in range(len(div_2)):
    df[n + i] = {'name': div_2[i].findChildren()[1].text.replace('\xa0', ' '),
                 'link': main_link_2 + div_2[i].findChildren()[1].get('href'),
                 'site': main_link_2, 
                 'min_salary': np.nan,
                 'max_salary': np.nan,
                 'currency': np.nan}

    salary = div_2[i].findChildren(recursive=False)[1].text.replace('\xa0', ' ')
    if salary != 'По договорённости':
        salary = salary.replace(' ', '')
        df[n + i]['currency'] = salary[-4:]
        if salary[:2] == 'от':
            df[n + i]['min_salary'] = int(re.findall('от([\d]*)', salary)[0])
        elif salary[:2] == 'до':
            df[n + i]['max_salary'] = int(re.findall('до([\d]*)', salary)[0])
        elif re.findall('—', salary):
            df[n + i]['min_salary'] = int(re.findall('([\d]*)—', salary)[0])
            df[n + i]['max_salary'] = int(re.findall('—([\d]*)', salary)[0])

pprint(df)

with open('vacancies.json', 'w') as outfile:
    json.dump(df, outfile)
