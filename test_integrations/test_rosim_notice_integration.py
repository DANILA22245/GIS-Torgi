import pytest
import requests
from jsonschema import validate, ValidationError
from conftest import (
    make_integration_request, generate_utc_timestamp,
    INTEGRATION_ENDPOINT, AUTH_TOKEN, DEFAULT_HEADERS
)

######################################################### Позитивные тесты ###################################################################
class TestNoticePositive:    
    @pytest.mark.parametrize("test_id,description,object_type", [
        ("P1", "Отправка валидного извещения", "BP"),
        ("P2", "Извещение с несколькими лотами", "BP"),
        ("P3", "Извещение по ПП РФ 1041", "BP"),
        ("P4", "Извещение с другим часовым поясом", "BP"),
        ("P5", "Повторная отправка с тем же rootId", "BP"),
        ("P6", "Извещеник с вложениями (после загрузки в ФХ)", "BP"),
        ("P7", "Реестр договоров objectType=RC", "RC"),
    ])
    def test_valid_notice_scenarios(self, valid_notice_fixture, api_session, 
                                   notice_schema, test_id, description, object_type):
        # Позитивные сценарии
        
        test_data = self._prepare_notice(valid_notice_fixture, test_id)
        try:
            validate(instance={"notice": test_data}, schema=notice_schema)
        except ValidationError as e:
            pytest.fail(f"[{test_id}] Schema validation failed: {e.message}")
        response = make_integration_request(
            api_session, 
            {"notice": test_data}, 
            object_type=object_type
        )
        
        
        assert response.status_code in [200, 202], \
            f"[{test_id}] Expected 200/202, got {response.status_code}\nResponse: {response.text}"
        
        resp_json = response.json()
        
        # Проверка структуры ответа
        assert "status" in resp_json or "refId" in resp_json, \
            "В ответе должен быть status или refId"
        
        if resp_json.get("status") == "PROCESSING":
            assert "refId" in resp_json, "refId может быть получен асинхронно путем вызова сервиса по специализированному адресу... (2.2.6)"
        elif resp_json.get("status") == "ACCEPTED":
            assert "loadId" in resp_json or "loadUrl" in resp_json, \
                "должен быть loadId или loadUrl"
    
    # Проверки
    def _prepare_notice(self, base: dict, scenario: str) -> dict:
        import copy
        
        if scenario == "P1":
            return copy.deepcopy(base)
            
        elif scenario == "P2":
            data = copy.deepcopy(base)
            
            data["lots"].append({
                "lotNumber": 2,
                "lotName": "Автомобиль УАЗ315196",
                "lotDescription": "Автомобиль УАЗ-315196, 2010 года выпуска, государственный номер Р662АЕ34, номер двигателя/шасси - А3016434/315100А0557548, VIN-ХТТ315196А0586785, цвет - Авантюрин металлик, паспорт транспортного средства - 73 МУ 481357",
                "priceMin": "1500000.00",
                "currency": {"code": "643"},
                "deposit": "75000.00",
                "biddingObjectInfo": {
                    "category": {"code": "9"},
                    "ownershipForms": {"code": "99"},
                    "estateAddressFIAS": {
                        "addressByFIAS": {"guid": "1ac46b49-3209-4814-b7bf-a509ea1aecd9"}
                    }
                }
            })
            return data
            
        elif scenario == "P3":
            # 229-ФЗ
            data = copy.deepcopy(base)
            data["commonInfo"]["biddType"]["code"] = "229FZ"
            data["commonInfo"]["biddForm"]["code"] = "EA"
            data["additionalDetails"] = [
                {"code": "DA_basis_EA(229)", "value": "Постановление судебного пристава"}
            ]
            return data
            
        elif scenario == "P4":
            data = copy.deepcopy(base)
            # +07:00
            data["biddConditions"]["biddStartTime"] = "2026-03-25T13:00:00+07:00"
            data["biddConditions"]["biddEndTime"] = "2026-04-06T09:00:00+07:00"
            return data
            
        elif scenario == "P5":
            # тот же rootId
            data = copy.deepcopy(base)
            data["rootId"] = "test-root-id-idempotent-12345"
            return data
            
        elif scenario == "P6":
            # Сначала загружаем в мок, потом указываем contentId
            data = copy.deepcopy(base)
            data["docs"] = [{
                "id": "doc-test-123",
                "name": "test.pdf",
                "size": 102400,
                "hash": "a" * 64,
                "contentId": "655348b3b6d4544c204ceb7b",  
                "attachmentType": {"code": "Notice_Document"}
            }]
            return data
            
        elif scenario == "P7":
            # РД
            data = copy.deepcopy(base)
            # Минимальный набор для РД
            data["commonInfo"]["biddType"]["code"] = "CONTRACT_REGISTRY"
            return data
            
        return copy.deepcopy(base)


######################################################### Негативные тесты ###################################################################

class TestNoticeSchemaValidation:
    
    @pytest.mark.parametrize("patch,expected_err_code,description", [
        # NRVE: Missing required fields
        ({"commonInfo": None}, "NRVE", "Отсутствует commonInfo"),
        ({"lots": []}, "NRVE", "Пустой массив lots (minItems=1)"),
        ({"lots": [{"lotName": "test"}]}, "NRVE", "Отсутствует lotNumber в лоте"),
        ({"timeZone": None}, "NRVE", "Отсутствует обязательный timeZone"),
        
        # XVE: Type mismatches
        ({"lots": [{"priceMin": 2352000}]}, "XVE", "priceMin должен быть строкой, не числом"),
        ({"biddConditions": {"biddStartTime": "25.03.2026"}}, "XVE", "Неверный формат даты"),
        ({"schemeVersion": "4.0"}, "XVE", "Неподдерживаемая версия схемы"),
        
        # IDE: Value constraints
        ({"lots": [{"lotNumber": 0}]}, "IDE", "lotNumber должен быть >= 1"),
        ({"lots": [{"lotName": ""}]}, "IDE", "lotName не может быть пустым"),
        ({"lots": [{"priceMin": "-100.00"}]}, "IDE", "Отрицательная цена"),
        
        # Справочники: invalid codes
        ({"commonInfo": {"biddType": {"code": "INVALID_FZ"}}}, "IDE", "Неверный код biddType"),
        ({"lots": [{"currency": {"code": "USD"}}]}, "IDE", "Неподдерживаемая валюта (только 643)"),
        ({"timeZone": {"code": "INVALID_TZ"}}}, "IDE", "Неверный код часового пояса"),
    ])
    def test_schema_validation_errors(self, valid_notice_fixture, api_session, 
                                     patch, expected_err_code, description):
        """Тесты на ошибки валидации схемы и данных"""
        
        test_data = apply_patch(valid_notice_fixture, patch)
        
        response = make_integration_request(api_session, {"notice": test_data})
        
        # По документации: ошибки валидации возвращают 400
        assert response.status_code == 400, \
            f"Expected 400 for {description}, got {response.status_code}"
        
        resp_json = response.json()
        
        # Проверка кода ошибки из раздела 4 документации
        err_code = resp_json.get("errCode") or (resp_json.get("errors", [{}])[0].get("errCode") if "errors" in resp_json else None)
        assert err_code == expected_err_code, \
            f"Expected errCode '{expected_err_code}' for {description}, got '{err_code}'\nResponse: {resp_json}"


# =============================================================================
# ❌ НЕГАТИВНЫЕ ТЕСТЫ — бизнес-правила (код ошибки: UBOE/EVE)
# =============================================================================

class TestNoticeBusinessRules:
    
    @pytest.mark.parametrize("patch,expected_err_code,description", [
        # Бизнес-ограничения
        ({"lots": [{"priceMin": "1000.00", "deposit": "5000.00"}]}, "UBOE", 
         "Задаток превышает начальную цену"),
        ({"biddConditions": {
            "biddStartTime": "2026-04-10T10:00:00Z",
            "biddEndTime": "2026-04-01T10:00:00Z"
        }}, "UBOE", "Дата окончания раньше даты начала"),
        
        # Ограничения на массивы
        ({"lots": [{"lotNumber": i} for i in range(1, 1001)]}, "UBOE", 
         "Превышено максимальное количество лотов (maxItems=999)"),
        
        # Форматы справочников
        ({"lots": [{"biddingObjectInfo": {
            "characteristics": [{"code": "cadastralNumberRealty", 
                               "characteristicValue": "54-35-INVALID"}]
        }}]}, "EVE", "Неверный формат кадастрового номера"),
        
        # Условные обязательные поля (например, для PPE)
        ({"commonInfo": {"biddForm": {"code": "PPE"}},
          "lots": [{"stagesImplementation": [{"stageNumber": 1}]}]}, "NRVE",
         "Для PPE требуется 4 этапа реализации (minItems=4)"),
    ])
    def test_business_rule_violations(self, valid_notice_fixture, api_session, 
                                     patch, expected_err_code, description):
        """Проверка бизнес-ограничений и условной валидации"""
        
        test_data = apply_patch(valid_notice_fixture, patch)
        response = make_integration_request(api_session, {"notice": test_data})
        
        assert response.status_code in [400, 422], \
            f"Expected 400/422 for {description}, got {response.status_code}"
        
        resp_json = response.json()
        err_code = resp_json.get("errCode") or (resp_json.get("errors", [{}])[0].get("errCode") if "errors" in resp_json else None)
        assert err_code == expected_err_code, \
            f"Expected '{expected_err_code}' for {description}, got '{err_code}'"


# =============================================================================
# ❌ НЕГАТИВНЫЕ ТЕСТЫ — технические и инфраструктурные
# =============================================================================

class TestNoticeTechnical:
    
    def test_missing_auth_token(self, valid_notice_fixture):
        """AE: Отсутствие auth_token"""
        headers = DEFAULT_HEADERS.copy()
        response = requests.post(
            INTEGRATION_ENDPOINT,
            headers=headers,
            params={},  # Нет auth_token
            json={"notice": valid_notice_fixture},
            timeout=30
        )
        assert response.status_code in [401, 403], "Expected 401/403 for missing auth"
    
    def test_wrong_content_type(self, valid_notice_fixture):
        """Неверный Content-Type"""
        headers = DEFAULT_HEADERS.copy()
        headers["Content-Type"] = "application/xml"
        
        response = requests.post(
            INTEGRATION_ENDPOINT,
            headers=headers,
            params={"auth_token": AUTH_TOKEN},
            json={"notice": valid_notice_fixture},
            timeout=30
        )
        # Может вернуть 415 или 400 в зависимости от реализации
        assert response.status_code in [400, 415], "Expected content-type error"
    
    def test_non_utf8_encoding(self, valid_notice_fixture):
        """Кодировка не UTF-8"""
        import json
        # Сериализуем в windows-1251 и отправляем без charset
        raw_data = json.dumps({"notice": valid_notice_fixture}, ensure_ascii=False).encode("windows-1251")
        
        headers = DEFAULT_HEADERS.copy()
        headers["Content-Type"] = "application/json"  # Без charset=utf-8
        
        response = requests.post(
            INTEGRATION_ENDPOINT,
            headers=headers,
            params={"auth_token": AUTH_TOKEN},
            data=raw_data,  # raw bytes, not json=
            timeout=30
        )
        # Ожидается ошибка парсинга или 400
        assert response.status_code in [400, 500], "Expected encoding error"
    
    def test_oversized_payload(self, valid_notice_fixture):
        """Превышение размера пакета (документация: ~1MB для AS2, для HTTPS — проверить лимит)"""
        # Добавляем большое поле в additionalDetails
        large_data = apply_patch(valid_notice_fixture, {
            "additionalDetails": [{"code": "TEST", "value": "x" * 2_000_000}]
        })
        
        response = make_integration_request(
            requests.Session(), 
            {"notice": large_data}
        )
        # Допустимые ответы: 413, 400 или 500
        assert response.status_code in [400, 413, 500], "Expected size limit error"
    
    def test_invalid_signature_format(self, valid_notice_fixture):
        """SGNE: Подпись не в формате CadES-BES / не Base64 / не GOST"""
        data_with_bad_sig = apply_patch(valid_notice_fixture, {
            "signedData": {
                "signature": "NOT_BASE64_!!!",  # Не валидный Base64
                "signatureType": "CadES-BES"
            }
        })
        
        response = make_integration_request(
            requests.Session(),
            {"notice": data_with_bad_sig}
        )
        # Ожидается ошибка подписи
        assert response.status_code == 400
        resp_json = response.json()
        err_code = resp_json.get("errCode")
        assert err_code == "SGNE", f"Expected SGNE for bad signature, got {err_code}"
    
    def test_attachment_without_contentId(self, valid_notice_fixture):
        """Вложение без contentId (файл не загружен в ФХ)"""
        data = apply_patch(valid_notice_fixture, {
            "docs": [{
                "id": "test-doc",
                "name": "file.pdf",
                "size": 1024,
                "hash": "a"*64,
                # contentId отсутствует!
                "attachmentType": {"code": "Notice_Document"}
            }]
        })
        
        response = make_integration_request(requests.Session(), {"notice": data})
        assert response.status_code == 400
        # Ожидается ошибка: файл не найден в ФХ
        resp_json = response.json()
        assert resp_json.get("errCode") in ["IDE", "EVE"], "Expected attachment validation error"


# =============================================================================
# 🔧 ВСПОМОГАТЕЛЬНЫЕ ТЕСТЫ
# =============================================================================

class TestNoticeUtilities:
    
    def test_schema_compliance_standalone(self, valid_notice_fixture, notice_schema):
        """Локальная проверка: фикстура проходит валидацию по схеме"""
        validate(instance={"notice": valid_notice_fixture}, schema=notice_schema)
    
    def test_datetime_utc_normalization(self):
        """Проверка формата дат: должны быть в UTC с миллисекундами"""
        from datetime import datetime, timezone
        ts = generate_utc_timestamp()
        # Проверка формата: 2026-03-25T13:00:00.000Z
        assert ts.endswith("Z"), "Timestamp must end with Z (UTC)"
        assert "." in ts, "Timestamp must include milliseconds"
        datetime.fromisoformat(ts.replace("Z", "+00:00"))  # Не должно упасть
    
    def test_money_fields_are_strings(self, valid_notice_fixture):
        """Проверка: денежные поля — строки, не числа"""
        for lot in valid_notice_fixture["lots"]:
            assert isinstance(lot["priceMin"], str), "priceMin must be string"
            if "deposit" in lot:
                assert isinstance(lot["deposit"], str), "deposit must be string"
            if "priceStep" in lot:
                assert isinstance(lot["priceStep"], str), "priceStep must be string"
    
    def test_response_time_under_limit(self, valid_notice_fixture, api_session):
        """Время ответа ≤ 120 сек (ограничение сессии по документации)"""
        import time
        start = time.time()
        response = make_integration_request(api_session, {"notice": valid_notice_fixture})
        elapsed = time.time() - start
        
        assert elapsed < 120, f"Response time {elapsed:.2f}s exceeds 120s limit"
        assert response.status_code in [200, 202, 400]  # Допустимые коды