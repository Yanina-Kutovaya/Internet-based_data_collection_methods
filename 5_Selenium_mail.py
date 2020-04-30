# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NewPassword172

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time


def authorization():
    login = 'study.ai_172@mail.ru'
    password = 'NewPassword172'

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://mail.ru/')

    name = driver.find_element_by_xpath("//input[@id='mailbox:login']")
    name.send_keys(login.split('@')[0])

    domain = driver.find_element_by_xpath("//select[@id='mailbox:domain']")
    options = domain.find_elements_by_tag_name('option')
    s = '@' + login.split('@')[1]
    for option in options:
        if option.text == s:
            select = Select(domain)
            select.select_by_visible_text(s)
            option.submit()

    password_input = driver.find_element_by_xpath("//input[@id='mailbox:password']")
    password_input.send_keys(password)
    password_input.submit()

    letters = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH,"//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")))
    assert 'Входящие - Почта Mail.ru' in driver.title

    return letters, driver


def scroll(letters, driver):
    action = ActionChains(driver)
    action.move_to_element(letters[-1])
    action.perform()
    letters = driver.find_elements_by_xpath(
        ".//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")
    return letters, driver


def get_text(driver):
    driver.get(letter.get_attribute('href'))
    content = WebDriverWait(driver, 10). \
        until(EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='WordSection1_mailru_css_attribute_postfix']")))
    assert 'Почта Mail.ru' in driver.title
    driver.back()
    time.sleep(5)
    assert 'Входящие - Почта Mail.ru' in driver.title
    return content[0].text, driver


if __name__ == '__main__':
    letters, driver = authorization()
    letters, driver = scroll(letters, driver)

    db = {}
    n = 0
    for letter in letters:
        df = {}
        df['author'] = letter.find_element_by_xpath(".//span[@class='ll-crpt']").text
        df['Re'] = letter.find_element_by_xpath(".//span[@class='ll-sj__normal']").text
        df['date'] = letter.find_element_by_xpath(".//div[@class='llc__item llc__item_date']").text
        #df['text'], driver = get_text(driver)
        db[n] = df
        n += 1
    driver.quit()

    client = MongoClient('localhost', 27017)
    mail = client['mail']
    db_list = []
    for i in db:
        db_list.append(db[i])
    mail.letters.insert_many([i for i in db_list])
