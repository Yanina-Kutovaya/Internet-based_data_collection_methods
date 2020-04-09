# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
from typing import Dict, Any, Union

import requests
import json
from pprint import pprint

username = 'Yanina-Kutovaya'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/80.0.3987.149 Safari/537.36'}
params = {'per_page': 30, 'page': 1}

response = requests.get('https://api.github.com/users/' + username + '/repos', headers=headers, params=params)

if response.ok:
    r = response.json()
    df = {}
    for i in range(len(r)):
        df['repository_' + str(i + 1)] = r[i]['name']
    pprint(df)

    with open('data.json', 'w') as outfile:
        json.dump(r, outfile)

# Reading json from file:
with open('data.json') as json_file:
    data = json.load(json_file)

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

link = "https://covid-193.p.rapidapi.com/statistics"

headers = {"x-rapidapi-host": 'covid-193.p.rapidapi.com',
           "x-rapidapi-key": "17977b0d24msh7b504747a5cc1e6p139faejsn2a2f5ef1bf71",
           "format": "json"}

response = requests.get(link, headers=headers)

if response.ok and 'json' in response.headers.get('Content-Type'):
    if 'json' in response.headers.get('Content-Type'):
        js = response.json()
        # dict_keys(['get', 'parameters', 'errors', 'results', 'response'])
        df = {}
        for i in range(len(js['response'])):
            country = js['response'][i]['country']
            if country[0] != '-':
                n_deaths = js['response'][i]['deaths']['total']
                df[country] = n_deaths
        deaths_list = sorted(df.items(), key=lambda kv: kv[1], reverse=True)[1:50]
        pprint(deaths_list)

        with open('covid_19.json', 'w') as outfile:
            json.dump(js, outfile)
    else:
        print('Response content is not in JSON format.')
        js = 'spam'


