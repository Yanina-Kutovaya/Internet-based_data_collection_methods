# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
# 3*. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

import json
import re
from pymongo import MongoClient
from pprint import pprint


def to_MongoDB(link, json_files):
    client = MongoClient('localhost', 27017)
    vacancies = client['vacancies']
    vacancies.Russia.delete_many({})  #################################
    for file in json_files:
        with open(link + file) as f:
            df = json.load(f)
        for i in df:
            vacancies.Russia.insert_one(df[i])
    return vacancies


def salary_query(limit):
    for i in vacancies.Russia.find({'$or': [{'min_salary': {'$gt': limit}}, {'max_salary': {'$gt': limit}}]}):
        pprint(i)


if __name__ == '__main__':
    link = 'C:/Users/ASER/PycharmProjects/internet_data_collection/'
    json_files = ['vacancies_1.json', 'vacancies_2.json']

    vacancies = to_MongoDB(link, json_files)

    limit = int(input('Введите минимально приемлемый уровень зарплаты: '))
    salary_query(limit)
    # for i in vacancies.Russia.find({'$or': [{'min_salary': {'$gt': limit}}, {'max_salary': {'$gt': limit}}]}):
    #    pprint(i)
