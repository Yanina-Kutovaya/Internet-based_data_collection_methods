#  Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
#  Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from pymongo import MongoClient
from pprint import pprint
import time


def parse_items(hit_sales, db):
    items = hit_sales.find_elements_by_tag_name('li')
    for item in items:
        df = {}
        df['name'] = item.find_elements_by_xpath(".//a[@data-product-info]")[1].text
        price = item.find_elements_by_xpath(".//div[@class='c-pdp-price__current']")[0].text[:-1]
        if df['name'] != '':
            df['price'] = int(price.replace(' ', ''))
            db.append(df)
    return db


def scroll(driver):    
    driver.find_elements_by_class_name('sel-hits-button-next')[2].click()
    time.sleep(5)
    hit_sales = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'accessories-product-list')))[2]
    return hit_sales, driver


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.mvideo.ru/')
    time.sleep(2)
    assert "М.Видео -" in driver.title

    db = []
    hit_sales = driver.find_elements_by_xpath("//ul[@class='accessories-product-list']")[2]
    db = parse_items(hit_sales, db)
    for i in range(3):
        hit_sales, driver = scroll(driver)
        db = parse_items(hit_sales, db)
    driver.quit()
    pprint(db)

    client = MongoClient('localhost', 27017)
    mvideo = client['mvideo']
    mvideo.sales_hits.insert_many([i for i in db])
