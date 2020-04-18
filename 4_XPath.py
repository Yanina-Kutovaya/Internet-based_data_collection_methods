# 1. Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
#    Для парсинга использовать xpath. Структура данных должна содержать:
#    •	название источника,
#    •	наименование новости,
#    •	ссылку на новость,
#    •	дата публикации
# 2. Сложить все новости в БД

import requests
import re
import datetime
from lxml import html
from pymongo import MongoClient
from pprint import pprint


def lenta_ru(headers, df):
    n = len(df)
    response = requests.get('https://lenta.ru', headers=headers)
    root = html.fromstring(response.text)
    items = root.xpath('//div[@class="b-tabloid__row row"][2]/div[1]/div[1]/div')

    pattern = re.compile('[\d]+/[\d]+/[\d]+')
    for i in range(1, len(items)):
        s = items[i].xpath('.//a/@href')[0]
        df[n + i - 1] = {'source': 'lenta.ru',
                         'link': 'https://lenta.ru' + s,
                         'date': datetime.datetime.strptime(pattern.findall(s)[0], '%Y/%m/%d').strftime('%d.%m.%Y')}
        if items[i].xpath('.//a/text()') != []:
            df[n + i - 1]['title'] = items[i].xpath('.//a/text()')[0].replace('\xa0', ' ')
        else:
            df[n + i - 1]['title'] = items[i].xpath('.//a/span//text()')[0].replace('\xa0', ' ')

    return df


def mail_ru(headers, df):
    n = len(df)
    response = requests.get('https://news.mail.ru', headers=headers)
    root = html.fromstring(response.text)
    s = "//div[@class='cols__inner']/div[@class='newsitem newsitem_height_fixed js-ago-wrapper']"
    df[n] = {'source': root.xpath(s + "//span[@class='newsitem__param']/text()")[1],
             'title': root.xpath(s + "//span[@class='newsitem__title-inner']/text()")[1],
             'link': 'https://news.mail.ru' + root.xpath(s + "//a/@href")[1],
             'date': root.xpath(s + "//span[@datetime]/text()")[1]}

    temp = root.xpath("//div[@class='cols__inner']/ul")[3]
    items = temp.xpath(".//li")
    for i in range(len(items)):
        df[n + i + 1] = {'link': 'https://news.mail.ru' + items[i].xpath(".//a/@href")[0],
                         'title': items[i].xpath(".//a/span/text()")[0].replace('\xa0', ' ')}
        r = requests.get(df[n + i + 1]['link'], headers=headers).text
        s = "//div[@class='breadcrumbs breadcrumbs_article js-ago-wrapper']"
        df[n + i + 1]['date'] = html.fromstring(r).xpath(s + "//span[@datetime]/text()")[0]
        df[n + i + 1]['source'] = html.fromstring(r).xpath(s + "//span[@class='link__text']/text()")[0]

    return df


def yandex_news(headers, df):
    n = len(df)
    response = requests.get('https://yandex.ru/news', headers=headers)
    root = html.fromstring(response.text)
    temp = root.xpath("//table[@class='stories-set__items']")[5]
    items = temp.xpath(".//td[@class='stories-set__item']")
    for i in range(len(items)):
        df[n + i] = {'date': datetime.datetime.today().date().strftime('%d.%m.%Y'),
                     'link': 'https://yandex.ru' + items[i].xpath(".//h2/a/@href")[0],
                     'sourse': items[i].xpath(".//div[@class='story__date']/text()")[0].split(' ')[0]}
        r = requests.get(df[n + i]['link'], headers=headers).text
        df[n + i]['title'] = html.fromstring(r).xpath("//span[@class='story__head-wrap']/text()")[0]

    return df


def news(headers):
    df = {}
    df = lenta_ru(headers, df)
    df = mail_ru(headers, df)
    df = yandex_news(headers, df)
    return df


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
               Chrome/80.0.3987.149 Safari/537.36'}
    df = news(headers)
    df_list = []
    for i in df:
        df_list.append(df[i])

    client = MongoClient('localhost', 27017)
    news = client['news']
    for i in df_list:
        news.main_news.update_one({'link': i['link']}, {'$set': i}, upsert=True)

    for i in news.main_news.find({}):
        pprint(i)
    print(news.main_news.count_documents({}))




