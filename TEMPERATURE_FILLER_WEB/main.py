import time
import sys
import random
from datetime import timedelta, date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

url = 'https://temptaking.ado.sg/group/urgroupid'
driverLocation = ""

users = [
    ['TEST NAME', 'userid', 'pin', date(2020, 4, 1), date(2020, 4, 2 + 1)],
    ['TEST NAME', 'userid', 'pin', None, None],
    # [name, userid, pin, start date, end date],
]

# Default start & end date
START_DATE = date(2020, 3, 16)
END_DATE = date(2020, 8, 13 + 1)

tempList = [360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370]
tempGradient = [-2, -1, 0, 1, 2]
timeoutSetting = 1


def load_browser(userid):

    browser = webdriver.Chrome(driverLocation)
    browser.get(url)

    wait = WebDriverWait(browser, timeoutSetting)

    name_select = Select(browser.find_element_by_id('member-select'))
    name_select.select_by_value(userid)
    time.sleep(0.1)

    return browser, wait


def reload_browser(browser, userid):
    browser.quit()
    load_browser(userid)


def randomtemp():
    return random.choices(tempList, weights=(2, 2, 6, 8, 18, 19, 23, 19, 5, 2, 2), k=1)[0]


def tempdiff():
    return random.choices(tempGradient, weights=(4, 24, 1, 24, 4), k=1)[0]


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def set_temp(browser, wait, userid, pin, date_str, clock, temp):
    time.sleep(0.1)
    try:
        pin_field = wait.until(ec.visibility_of_element_located((By.XPATH, '//input[@id="ep1"]')))
        pin_field.send_keys(pin+temp)

        date_field = wait.until(ec.visibility_of_element_located((By.XPATH, '//input[@id="date-input"]')))
        date_field.send_keys(date_str)

        time_field = wait.until(ec.visibility_of_element_located((By.XPATH, '//select[@id="meridies-input"]')))
        # time_field = Select(browser.find_element_by_id('meridies-input'))
        # time_field.select_by_value(clock)
        time_field.send_keys(clock)

        submit_btn = wait.until(ec.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-warning"]')))
        ActionChains(browser).click(submit_btn).perform()

        confirm_btn = wait.until(ec.visibility_of_element_located((By.XPATH, '//button[@id="submit-temp-btn"]')))
        ActionChains(browser).click(confirm_btn).perform()

        time.sleep(0.1)
        back_btn = wait.until(ec.visibility_of_element_located((By.XPATH, '//button[text()="BACK"]')))
        # back_btn = browser.find_element_by_xpath('//button[@class="btn btn-warning"]')
        ActionChains(browser).click(back_btn).perform()

    except:
        print('Something went wrong (' + date_str + ' ' + clock + ') \n', sys.exc_info())
        reload_browser(browser, userid)
        set_temp(browser, wait, userid, pin, date_str, clock, temp)
    else:
        print(date_str + " " + clock, temp)
    return


def handle_user(name, userid, pin, start_date, end_date):
    print("Init", name + '(' + userid + ')', 'PIN: ' + pin)

    start_time = time.perf_counter()
    start_date = start_date and start_date or START_DATE
    end_date = end_date and end_date or END_DATE

    browser, wait = load_browser(userid)

    for single_date in date_range(start_date, end_date):
        date_str = single_date.strftime("%m/%d/%Y")
        initial_temp = randomtemp()

        set_temp(browser, wait, userid, pin, date_str, 'AM', str(initial_temp))
        set_temp(browser, wait, userid, pin, date_str, 'PM', str(initial_temp + tempdiff()))

    print("Finished for " + name + " Time elapsed: " + str(time.perf_counter() - start_time))
    browser.quit()


for user in users:
    handle_user(user[0], user[1], user[2], user[3], user[4])

print("Executed successfully")
