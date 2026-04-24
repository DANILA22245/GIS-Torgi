import requests
import pytest


# Проверки на работоспособность открытой части
def test_main_page():
    main_page = requests.get("https://torgi.gov.ru/new/public", timeout=10)
    assert main_page.status_code == 200


def test_lots():
    lots = requests.get("https://torgi.gov.ru/new/public/lots/reg", timeout=10)
    assert lots.status_code == 200


def test_notices():
    notices = requests.get("https://torgi.gov.ru/new/public/notices/reg", timeout=10)
    assert notices.status_code == 200


def test_old_version():
    old = requests.get("https://torgi.gov.ru/new/public/op/reg", timeout=10)
    assert old.status_code == 200


def test_privatization():
    privatization = requests.get(
        "https://torgi.gov.ru/new/public/privatization-plans/reg/(list:plans)",
        timeout=10,
    )
    assert privatization.status_code == 200


def test_federalnoe():
    federalnoe = requests.get(
        "https://torgi.gov.ru/new/public/privatization-plans/reg/(list:ks)", timeout=10
    )
    assert federalnoe.status_code == 200


def test_decision():
    decision = requests.get(
        "https://torgi.gov.ru/new/public/privatization-plans/reg/(list:decision)",
        timeout=10,
    )
    assert decision.status_code == 200


def test_reports():
    reports = requests.get(
        "https://torgi.gov.ru/new/public/privatization-plans/reg/(list:reports)",
        timeout=10,
    )
    assert reports.status_code == 200


def test_concess():
    concess = requests.get("https://torgi.gov.ru/new/public/objects/reg", timeout=10)
    assert concess.status_code == 200


def test_earth():
    prison_earth_users = requests.get(
        "https://torgi.gov.ru/new/public/rny/reg/(list:earth)", timeout=10
    )
    assert prison_earth_users.status_code == 200


def test_bowels():
    prison_bowels_users = requests.get(
        "https://torgi.gov.ru/new/public/rny/reg/(list:bowels)", timeout=10
    )
    assert prison_bowels_users.status_code == 200


def test_fishery():
    prison_fishery_users = requests.get(
        "https://torgi.gov.ru/new/public/rny/reg/(list:fishery)", timeout=10
    )
    assert prison_fishery_users.status_code == 200


def test_appeals():
    appeals = requests.get("https://torgi.gov.ru/new/public/appeals/reg", timeout=10)
    assert appeals.status_code == 200


def test_contracts():
    contracts = requests.get(
        "https://torgi.gov.ru/new/public/contracts/reg", timeout=10
    )
    assert contracts.status_code == 200


def test_organizations():
    organizations = requests.get(
        "https://torgi.gov.ru/new/public/organizations/reg", timeout=10
    )
    assert organizations.status_code == 200


def test_opendata():
    opendata = requests.get("https://torgi.gov.ru/new/public/opendata/reg", timeout=10)
    assert opendata.status_code == 200


def test_legislation():
    legislation = requests.get(
        "https://torgi.gov.ru/new/public/legislation/reg", timeout=10
    )
    assert legislation.status_code == 200


def test_widgets():
    widgets = requests.get("https://torgi.gov.ru/new/public#widgets", timeout=10)
    assert widgets.status_code == 200


def test_support():
    support = requests.get(
        "https://torgi.gov.ru/new/cabinet/support/center", timeout=10
    )
    assert support.status_code == 200


def test_esia():
    esia = requests.get("https://esia.gosuslugi.ru/login/", timeout=10)
    assert esia.status_code == 200


def test_map():
    map = requests.get(
        "https://torgi.gov.ru/new/public/realizable-estate-on-the-map/reg", timeout=10
    )
    assert map.status_code == 200


def test_about():
    about = requests.get("https://torgi.gov.ru/new/public/about/reg", timeout=10)
    assert about.status_code == 200


def test_questions():
    questions = requests.get(
        "https://torgi.gov.ru/new/public/questions/reg", timeout=10
    )
    assert questions.status_code == 200


def test_infomaterials():
    infomaterials = requests.get(
        "https://torgi.gov.ru/new/public/infomaterials/reg", timeout=10
    )
    assert infomaterials.status_code == 200
# Проверки на работоспособность открытой части
