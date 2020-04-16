import math
import numpy as np
import json
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def fillna(value, default=0):
    if math.isnan(value):
        return default
    return value


def zero_to_nan(value):
    if value == 0:
        return np.nan
    else:
        return value


engine = create_engine('sqlite:///vacancies.db', echo=True)
Base = declarative_base()


class Vacancies(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    vacancy_id = Column(String(120))
    name = Column(String(255))
    link = Column(String(255))
    site = Column(String(120))
    min_salary = Column(Integer)
    max_salary = Column(Integer)
    currency = Column(String(120))

    def __init__(self, vacancy_id, name, link, site, min_salary, max_salary, currency):
        self.vacancy_id = vacancy_id
        self.name = name
        self.link = link
        self.site = site
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.currency = currency


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

link = 'C:/Users/ASER/PycharmProjects/internet_data_collection/'
json_files = ['vacancies_1.json', 'vacancies_2.json']
data = []
for file in json_files:
    with open(link + file) as f:
        df = json.load(f)
        for i in df:
            s = Vacancies(df[i]['id'],
                          df[i]['name'],
                          df[i]['link'],
                          df[i]['site'],
                          fillna(df[i]['min_salary'], default=0),
                          fillna(df[i]['max_salary'], default=0),
                          df[i]['currency'])
            data.append(s)

session = Session()
session.add_all(data)

limit = int(input('Введите минимально приемлемый уровень зарплаты: '))
for instanse in session.query(Vacancies).filter((Vacancies.min_salary > limit) | (Vacancies.max_salary > limit)):
    print(instanse.name, 'зарплата: ', zero_to_nan(instanse.min_salary), '-', zero_to_nan(instanse.max_salary),
          instanse.link)

session.commit()
session.close()