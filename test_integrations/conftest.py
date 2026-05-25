# tests/conftest.py
import os
import json
import pytest
import requests
from datetime import datetime, timezone



BASE_URL = os.getenv("GIS_TORGI_BASE_URL", "https://demo.torgi.gov.ru/")
INTEGRATION_ENDPOINT = f"{BASE_URL}/new/integration-rest-adapter/packets"
AUTH_TOKEN = os.getenv("GIS_TORGI_AUTH_TOKEN", "токен")
DEFAULT_HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json"
}

#Грузим схему 
@pytest.fixture(scope="session")
def notice_schema():
    schema_path = r'C:\Users\Олег\Desktop\torgi\test_integrations\schemas\Notice.json'
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)
#Грузим схему

#Грузим валидный json от Росимущества
@pytest.fixture(scope="session")
def valid_notice_fixture():
    fixture_path = r'C:\Users\Олег\Desktop\torgi\test_integrations\fixtures\valid_notice.json'
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)
#Грузим валидный json от Росимущества


#Дефолтные настройки сессии (у нас таймаут максимальный 120)
@pytest.fixture
def api_session():    
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    session.timeout = 120  
    yield session
    session.close()
#Дефолтные настройки сессии (у нас таймаут максимальный 120)


#Параметры авторизации для запросов
@pytest.fixture
def auth_params():
    return {"auth_token": AUTH_TOKEN}
#Параметры авторизации для запросов


#Отправка пакетов
def make_integration_request(session, data, params=None, object_type="BP"):
    url = INTEGRATION_ENDPOINT
    if params is None:
        params = {"auth_token": AUTH_TOKEN, "objectType": object_type}
    else:
        params.setdefault("auth_token", AUTH_TOKEN)
        params.setdefault("objectType", object_type)    
    return session.post(url, json=data, params=params, timeout=120)
#Отправка пакетов


#Отправляем текущее время по маске
def generate_utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
#Отправляем текущее время по маске


