import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import requests

accounts = [{'log' : '530-714-117 43', 'pass' : 'Test!12345', 'statuscode' : 200},
            {'log' : '000-918-546 77', 'pass' : ',!MO80is', 'statuscode' : 200},
            {'log' : '000-360-720 55', 'pass' : 'tKz(7UB_=8', 'statuscode' : 200},
            {'log' : '000-022-440 00', 'pass' : '8mNEPy11)', 'statuscode' : 200},
            {'log' : '000-000-600 55', 'pass' : '11111111', 'statuscode' : 200},
            {'log' : '000-000-600 29', 'pass' : '11111111', 'statuscode' : 200},
            {'log' : '000-360-720 55', 'pass' : 'tKz(7UB_=8', 'statuscode' : 200},
            {'log' : '000-000-600 20', 'pass' : '11111111', 'statuscode' : 200},
            {'log' : '000-000-600 07', 'pass' : '11111111', 'statuscode' : 200},
            {'log' : '000 546 648 17', 'pass' : '6!c5vU~%=N', 'statuscode' : 200},
            {'log' : '000-003-336 00', 'pass' : 'og2k6RD::', 'statuscode' : 200},        
            ]

@pytest.fixture(scope="function")
def driver():
    service = Service(r"C:\Users\Олег\Desktop\torgi\msedgedriver.exe")
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(',хттпс//базовая авторизация')
    yield driver
    driver.quit()

@pytest.mark.parametrize("account", accounts, ids=lambda x: x["log"])
def test_account_flow(driver, account):
    enter = driver.find_element(By.XPATH, "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-public-shell/div/div/app-public-main/div[1]/app-main-header/div/div/div/div[3]/app-login/app-button/button/span[2]")
    enter.click()
    login = driver.find_element(By.XPATH, "//*[@id='login']")
    login.send_keys(account['log'])
    password = driver.find_element(By.XPATH, "//*[@id='password']")
    password.send_keys(account['pass'])
    authorise = driver.find_element(By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[3]/button")
    authorise.click()
    driver.implicitly_wait(2)
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get(driver.current_url)

    assert response.status_code == account['statuscode']
        