from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha

import math
import time

driver = webdriver.Chrome('/Users/macbook/Desktop/Computer/Ect/chromedriver')
options = webdriver.ChromeOptions()

options.add_argument("disable-gpu")  # 가속 사용 x
options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재

driver.get('https://sugang.kmu.ac.kr/servlet/Fip')

account = ['id', 'pw']
codes = [['26830', '02'], ['41989', '02'], ['26836', '02']]
test = [['21235', '02'], ['26456', '01'], ['20815', '02']]


# test front code 21235


def log_in():
    id_form = driver.find_element_by_id('a_id')
    pw_form = driver.find_element_by_id('a_pw')

    id_form.send_keys(account[0])
    pw_form.send_keys(account[1])

    driver.execute_script("javascript:qrySubmit()")


def move_into_frame():
    frame = driver.find_element_by_name('top')
    driver.switch_to.frame(frame)


def solve_captcha():
    captcha_png = driver.find_element_by_xpath(
        '/html/body/div/div[3]/div[1]/div[3]/table/tbody/tr/td[1]/div/span/img').screenshot_as_png
    with open('captcha.png', 'wb') as file:
        file.write(captcha_png)

    api_key = ''
    solver = TwoCaptcha(api_key)

    start = time.time()

    try:
        result = solver.normal('captcha.png')
        result_code = result['code']
    except Exception as e:
        driver.close()

    end = time.time()
    print(f"{end - start:.5f} sec")

    result_elem = driver.find_element_by_id('refCaptcha')
    result_elem.send_keys(result_code)


def add_course(index):
    first_code_form = driver.find_element_by_name('a_sc_cd')
    second_code_form = driver.find_element_by_name('a_lt_no')

    first_code_form.send_keys(test[index][0])
    second_code_form.send_keys(test[index][1])
    print(test[index])

    submit = driver.find_element_by_xpath("//table[@class='table_search1']/tbody/tr/form")

    submit.submit()


def handle_alert():
    alert = driver.switch_to.alert
    alert.accept()


def mecro():
    log_in()
    move_into_frame()
    for index in range(3):
        solve_captcha()
        add_course(index)
        handle_alert()

    # move_into_frame()
    # solve_captcha()
    # add_course(1)
    # handle_alert()


def open_new_tab(index):
    # move_into_frame()
    # target = driver.find_element_by_tag_name('body')
    # print(target)
    # target.send_keys(Keys.COMMAND + 't')
    driver.execute_script("window.open('https://sugang.kmu.ac.kr/servlet/Fip')")
    # driver.Url = 'https://sugang.kmu.ac.kr/servlet/Fip'


mecro()
