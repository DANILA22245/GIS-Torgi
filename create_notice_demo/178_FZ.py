from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# базовая авторизация на стенде
service = Service(r"C:\Users\Олег\Desktop\torgi\msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.maximize_window()
driver.get(
    "https://prod:SFJpnasgeE8fwxr7D4VAxV6uPiMXZ2Sn8kDgwg54EcKUsN4jSuPHbWxU2hjQmL99@demo.torgi.gov.ru/new/public"
)
driver.implicitly_wait(100)
# базовая авторизация на стенде

# авторизация под Николаем Николаевичем
enter = driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-public-shell/div/div/app-public-main/div[1]/app-main-header/div/div/div/div[3]/app-login/app-button/button/span[2]",
)
enter.click()
login = driver.find_element(By.XPATH, "//*[@id='login']")
login.send_keys("000-022-440 00")
password = driver.find_element(By.XPATH, "//*[@id='password']")
password.send_keys("8mNEPy11)")
authorise = driver.find_element(
    By.XPATH, "/html/body/esia-root/div/esia-login/div/div[1]/form/div[3]/button"
)
authorise.click()
# авторизация под Николаем Николаевичем

# Создание извещения
organizator = driver.find_element(
    By.XPATH,
    "/html/body/ngb-modal-window/div/div/app-organization-select-modal/div[2]/div[1]/div/div[4]/app-big-radio-button[1]/label/span",
)
organizator.click()
driver.find_element(
    By.XPATH,
    "/html/body/ngb-modal-window/div/div/app-organization-select-modal/div[3]/app-button[2]/button/span[2]",
).click()
driver.find_element(
    By.XPATH,
    "/html/body/ngb-modal-window/div/div/app-organization-select-modal/div[2]/div/div/div[4]/ul/li[2]/div[1]/span",
).click()
driver.find_element(
    By.XPATH,
    "/html/body/ngb-modal-window/div/div/app-organization-select-modal/div[3]/app-button[2]/button/span[2]",
).click()
driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div[1]/aside/app-private-menu/div/div/div/div[8]/div/app-private-menu-item/div/a/span",
).click()
driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div[1]/div/app-notice-list/div[1]/div/app-button/a/span[2]",
).click()
driver.find_element(
    By.XPATH, '//*[@id="noticeBiddType"]/ng-select/div/div/div[1]'
).click()
wait = WebDriverWait(driver, 10)
noticeBiddType = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//span[contains(text(), "Продажа (приватизация) государственного и муниципального имущества")]',
        )
    )
)
noticeBiddType.click()
driver.find_element(
    By.XPATH, '//*[@id="noticeBiddForm"]/ng-select/div/div/div[1]'
).click()
noticeBiddForm = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[contains(text(), "Электронный аукцион")]')
    )
)
noticeBiddForm.click()
driver.find_element(
    By.XPATH, '//*[@id="noticeEtpCode"]/ng-select/div/div/div[1]'
).click()
ETP = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//span[contains(text(), "АКЦИОНЕРНОЕ ОБЩЕСТВО «ЕДИНАЯ ЭЛЕКТРОННАЯ ТОРГОВАЯ ПЛОЩАДКА»")]',
        )
    )
)
ETP.click()
driver.find_element(By.XPATH, '//*[@id="noticeProcedureName"]/div').send_keys(
    "Polyak_test_178"
)
driver.find_element(
    By.XPATH,
    '//*[@id="noticeBaseDynamicAttr2-DA_tradingFeatures_EA(178)"]/ng-select/div',
).click()
osobennost = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//span[contains(text(), "Реализация древесины в соответствии со ст. 43 - 46 ЛК РФ")]',
        )
    )
)
osobennost.click()
create_lot = driver.find_element(By.XPATH, "//*[@id='addLot']/span[2]")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", create_lot)
time.sleep(0.3)
create_lot.click()
driver.find_element(By.XPATH, '//*[@id="noticeLot-0-privatizationReason"]').send_keys(
    "Мин Поляк России"
)
driver.find_element(By.XPATH, '//*[@id="noticeLot-0-lotName"]/div').send_keys("Stone")
driver.find_element(By.XPATH, '//*[@id="noticeLot-0-lotDescription"]/div').send_keys(
    "Big_Stone"
)
driver.find_element(By.XPATH, '//*[@id="noticeLot-0-priceMin"]').send_keys("1000000")
driver.find_element(By.XPATH, '//*[@id="noticeLot-0-priceStep"]').send_keys("100000")
driver.find_element(
    By.XPATH, '//*[@id="noticeLot-0-lotVat"]/ng-select/div/div/div[1]'
).click()
NDS = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[contains(text(), "НДС не облагается")]')
    )
)
NDS.click()
driver.find_element(By.XPATH, '//*[@id="noticeLot-0-deposit"]').send_keys("100000")
driver.find_element(
    By.XPATH, '//*[@id="noticeLot-0-account-accountNumber"]/ng-select/div'
).click()
ploshadka = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[contains(text(), "Счет 40702810510050001273")]')
    )
)
ploshadka.click()

GAR = driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div/div/app-notice-edit-form/div/div[1]/div[6]/div[2]/div[2]/div[3]/app-notice-edit-form-lot-info/div[5]/app-fias-search-area/div/div[1]/app-form-item/div/div[2]/app-input/div/input",
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", GAR)
time.sleep(0.3)
GAR.send_keys("111")
Adress = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            '//span[contains(text(), "респ. Удмуртская, м.о. Завьяловский район, тер. ГСК АгроТЭП, дом 111/113/111а")]',
        )
    )
)
Adress.click()
driver.find_element(
    By.XPATH, '//*[@id="noticeLot-0-ownershipForm"]/ng-select/div/div/div[1]'
).click()
Bidd = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[contains(text(), "Федеральная собственность")]')
    )
)
Bidd.click()

start_date = driver.find_element(By.XPATH, '//*[@id="noticeBiddStartTime"]')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", create_lot)
time.sleep(0.3)
start_date.click()
driver.find_element(
    By.XPATH,
    "/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div/div/app-notice-edit-form/div/div[1]/div[8]/app-notice-edit-form-procedure-requirements-info/div[1]/div[1]/app-form-item/div/div[2]/app-datetime-input/div/div[2]/div[1]/ngb-datepicker/div[2]/div/ngb-datepicker-month/div[4]/div[4]/span",
).click()

driver.find_element(By.XPATH, '//*[@id="noticeBiddEndTime"]').click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div/div/app-notice-edit-form/div/div[1]/div[8]/app-notice-edit-form-procedure-requirements-info/div[1]/div[2]/app-form-item/div/div[2]/app-datetime-input/div/div[2]/div[1]/ngb-datepicker/div[2]/div/ngb-datepicker-month/div[6]/div[3]/span').click()

noticeBiddReviewDate = driver.find_element(By.XPATH, '//*[@id="noticeBiddReviewDate"]')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", create_lot)
time.sleep(0.3)
noticeBiddReviewDate.click()

driver.find_element(By.XPATH, '/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div/div/app-notice-edit-form/div/div[1]/div[8]/app-notice-edit-form-procedure-requirements-info/div[2]/div[1]/app-form-item/div/div[2]/app-datetime-input/div/div[2]/div/ngb-datepicker/div[2]/div/ngb-datepicker-month/div[6]/div[3]/span').click()   
driver.find_element(By.XPATH, '//*[@id="noticeAuctionStartDate"]').click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div/div/app-notice-edit-form/div/div[1]/div[8]/app-notice-edit-form-procedure-requirements-info/div[2]/div[2]/app-form-item/div/div[2]/app-datetime-input/div/div[2]/div[1]/ngb-datepicker/div[2]/div/ngb-datepicker-month/div[7]/div[4]/span').click()


#Добавление файла - основания
file = r'Q:\мусор\описание для мобилки.pdf'
file_input = driver.find_elements(By.XPATH, '//*[@id="fileDropRef"]')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", file_input[3])
time.sleep(0.3)
file_input[3].send_keys(file)
driver.find_element(By.XPATH, '//*[@id="noticeDocAttachments"]/div/app-hashed-attachments-list/div/div/div/div[2]/app-form-item/div/div[2]/app-select/ng-select/div/div/div[1]').click()
document = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[contains(text(), "Проект договора")]')
    )
)
document.click()
#Добавление файла - основания
category = driver.find_element(
    By.XPATH,
    "//*[@id='noticeLot-0-chooseCategory']/span[2]",
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category)
time.sleep(0.3)
category.click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/ngb-modal-window/div/div/app-category-select/app-modal-content/div/div[1]/div[2]/div[2]/div/ul/li[7]/span').click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/ngb-modal-window/div/div/app-category-select/app-modal-content/div/div[1]/div[2]/div[2]/div/ul[2]/li[7]/span').click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/ngb-modal-window/div/div/app-category-select/app-modal-content/div/div[2]/div/app-button[2]/button/span[2]').click()

#Добавление фото лота
file_lot = r'Q:\мусор\1666713195_12-7fon-club-p-gachimuchi-oboi-12.jpg'
file_input_lot = driver.find_elements(By.XPATH, '//*[@id="fileDropRef"]')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", file_input_lot[0])
time.sleep(0.3)
file_input_lot[0].send_keys(file_lot)
#Добавление фото лота

driver.find_element(By.XPATH, '//*[@id="noticeLot-0-characteristic-quantityWood"]/div').send_keys('19000')
# Создание извещения


#Извещение СОЗДАНО

#Сохранить извещение
driver.find_element(By.XPATH, '//*[@id="saveNotice"]/span[2]').click()
driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/app-pub-entity-validation-results/app-modal-content/div/div[2]/div/div[2]/app-button/button/span[2]').click()
#Сохранить извещение



#Удалить извещение
driver.find_element(By.XPATH, '//*[@id="noticeRegistryGobackLink"]/span[2]').click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div[1]/div/app-notice-list/app-notice-list-sort/div/app-button[1]/div/button/span[2]').click()
driver.find_element(By.XPATH, '/html/body/app-root/app-layout/main/app-work-area/div/div/div/app-private-shell/div[1]/div/app-notice-list/app-notice-list-sort/div/app-button[1]/div/div/div[2]/button/div/div[1]/div').click()
driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/app-pub-delete-confirm-dialog/app-modal-content/div/div[2]/div/div[2]/app-button[1]/button/span[2]').click()
#Удалить извещение


input()
