#  Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
#  Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pprint import pprint
import time


def parse_items(hit_sales, db):
    items = hit_sales.find_elements_by_tag_name('li')
    n = len(db)
    for item in items:
        df = {}
        name = item.find_elements_by_xpath(".//a[@data-product-info]")[1].text
        price = int(item.find_elements_by_xpath(".//div[@class='c-pdp-price__current']")[0].text[:-1].replace(' ', ''))
        df['name'] = name
        df['price'] = price
        db[n] = df
        n += 1
    return db


def scroll(hit_sales, driver):
    time.sleep(3)
    if hit_sales.find_element_by_xpath(".//a[@class='next-btn sel-hits-button-next']"):
        action = ActionChains(driver)
        action.move_to_element(hit_sales.find_element_by_xpath(".//a[@class='next-btn sel-hits-button-next']"))
        action.click()
        hit_sales = driver.find_elements_by_xpath("//div[@class='accessories-carousel-wrapper']")[2]
        return hit_sales, driver


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.mvideo.ru/')

    hit_sales = driver.find_elements_by_xpath("//div[@class='accessories-carousel-wrapper']")[2]
    db = {}
    db = parse_items(hit_sales, db)
    for i in range(3):
        hit_sales, driver = scroll(hit_sales, driver)
        db = parse_items(hit_sales, db)
    driver.quit()
    pprint(db)

    client = MongoClient('localhost', 27017)
    mvideo = client['mvideo']
    db_list = []
    for i in db:
        db_list.append(db[i])
    mvideo.sales_hits.insert_many([i for i in db_list])

