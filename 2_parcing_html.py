# Необходимо собрать информацию о вакансиях на вводимую должность с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:

# - Наименование вакансии
# - Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
# - Ссылку на саму вакансию
# - Сайт откуда собрана вакансия

# Данная структура должна быть одинаковая для вакансий с обоих сайтов.

import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import re
import json
from pprint import pprint


def set_params(position, page_n):
    params_1 = {'text': position,
                'page': page_n}

    params_2 = {'keywords': position,
                'page': page_n}

    site_dict = {'0': {'main_link': 'https://hh.ru',
                       'link': '/search/vacancy',
                       'params': params_1,
                       'div_class': "vacancy-serp-item__row vacancy-serp-item__row_header",
                       'child_n': 4,
                       'link_prefix': '',
                       'empty_clause': '',
                       's_str': '-'},
                 '1': {'main_link': 'https://russia.superjob.ru',
                       'link': '/vacancy/search',
                       'params': params_2,
                       'div_class': "acdxh GPKTZ _1tH7S",
                       'child_n': 1,
                       'link_prefix': 'https://russia.superjob.ru',
                       'empty_clause': 'По договорённости',
                       's_str': '—'}}

    return site_dict


def page_data(df, site_id, position, page_n, headers):
    site_dict = set_params(position, page_n)

    url = f"{site_dict[site_id]['main_link']}{site_dict[site_id]['link']}"
    response = requests.get(url, headers=headers, params=site_dict[site_id]['params']).text

    soap = bs(response, 'lxml')
    div = soap.find_all('div', {'class': site_dict[site_id]['div_class']})
    child_n = site_dict[site_id]['child_n']
    empty_clause = site_dict[site_id]['empty_clause']
    s_str = site_dict[site_id]['s_str']

    n = len(df)
    for i in range(len(div)):
        df[n + i] = {'name': div[i].findChildren()[child_n].text.replace('\xa0', ' '),
                     'link': site_dict[site_id]['link_prefix'] + div[i].findChildren()[child_n].get('href'),
                     'site': site_dict[site_id]['main_link'],
                     'min_salary': np.nan,
                     'max_salary': np.nan,
                     'currency': np.nan}

        salary = div[i].findChildren(recursive=False)[1].text
        if salary != empty_clause:
            df[n + i]['currency'] = salary[-4:].replace(' ', '')

            salary = salary.replace('\xa0', '').replace(' ', '')
            if salary[:2] == 'от':
                df[n + i]['min_salary'] = int(re.findall('от([\d]*)', salary)[0])
            elif salary[:2] == 'до':
                df[n + i]['max_salary'] = int(re.findall('до([\d]*)', salary)[0])
            elif re.findall(s_str, salary):
                df[n + i]['min_salary'] = int(re.findall('([\d]*)' + s_str, salary)[0])
                df[n + i]['max_salary'] = int(re.findall(s_str + '([\d]*)', salary)[0])

    return site_dict, soap, df


def data_from_site(n_of_pages, site_id, position, headers):
    df = {}
    page_n = 0
    site_dict, soap, df = page_data(df, site_id, position, page_n, headers)
    for i in range(1, n_of_pages):
        if site_id == '0':
            try:
                if soap.find_all('div', {'data-qa': "pager-block"})[0].findChildren()[-2].text == 'дальше':
                    page_n += 1
                    site_dict, soap, df = page_data(df, site_id, position, page_n, headers)
                else:
                    print(f'Число страниц сайта, соответствующих запросу: {page_n + 1}.')
                    return df
            except:
                print(f'Число страниц сайта, соответствующих запросу: {page_n + 1}.')
                return df

        elif site_id == '1':
            try:
                if soap.find_all('div', {'class': "L1p51"})[0].findChildren()[-1].text == 'Дальше':
                    page_n += 1
                    site_dict, soap, df = page_data(df, site_id, position, page_n, headers)
                else:
                    print(f'Число страниц сайта, соответствующих запросу: {page_n + 1}.')
                    return df
            except:
                print(f'Число страниц сайта, соответствующих запросу: {page_n + 1}.')
                return df
    return df


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
               Chrome/80.0.3987.149 Safari/537.36'}

    site_id = input('Введите 0 для сайта hh.ru или 1 для сайта superjob: ')
    position = input('Введите позицию, по которой будет осуществляться поиск: ')
    n_of_pages = int(input('Введите число страниц с сайта, которoе Вы планируете проанализировать: '))

    df = data_from_site(n_of_pages, site_id, position, headers)
    pprint(df)

    with open('vacancies.json', 'w') as outfile:
        json.dump(df, outfile)
