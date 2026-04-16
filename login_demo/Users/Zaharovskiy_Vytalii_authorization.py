from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

#базовая авторизация на стенде
service = Service(r"C:\Users\Олег\Desktop\torgi_test\msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.maximize_window()
driver.get('https://prod:SFJpnasgeE8fwxr7D4VAxV6uPiMXZ2Sn8kDgwg54EcKUsN4jSuPHbWxU2hjQmL99@demo.torgi.gov.ru/new/public')
driver.implicitly_wait(100)
#базовая авторизация на стенде

#авторизация под Захаровским Виталием
enter = driver.find_element(By.XPATH, "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-public-shell/div/div/app-public-main/div[1]/app-main-header/div/div/div/div[3]/app-login/app-button/button/span[2]")
enter.click()
login = driver.find_element(By.XPATH, "//*[@id='login']")
login.send_keys("000-918-546 77")
password = driver.find_element(By.XPATH, "//*[@id='password']")
password.send_keys(",!MO80is")
authorise = driver.find_element(By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[3]/button")
authorise.click()
#авторизация под Захаровским Виталием

