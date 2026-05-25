import pytest
import json
import copy
import requests
from pathlib import Path

url = "https://сбер" 
token = "токен"
HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}",
    "User-Agent": "торги"
}



REQUIRED = [
    "index.id",
    "index.sender",
    "index.receiver",
    "index.requestDate",
    "index.objectType",
    "index.objectId",
    "data.structuredObject.notice.schemeVersion",
    "data.structuredObject.notice.id",
    "data.structuredObject.notice.rootId",
    "data.structuredObject.notice.version",
    "data.structuredObject.notice.commonInfo",
    "data.structuredObject.notice.commonInfo.noticeNumber",
    "data.structuredObject.notice.commonInfo.biddType",
    "data.structuredObject.notice.commonInfo.biddType.code",
    "data.structuredObject.notice.commonInfo.biddType.name",
    "data.structuredObject.notice.commonInfo.biddForm",
    "data.structuredObject.notice.commonInfo.biddForm.code",
    "data.structuredObject.notice.commonInfo.biddForm.name",
    "data.structuredObject.notice.commonInfo.publishDate",
    "data.structuredObject.notice.commonInfo.procedureName",
    "data.structuredObject.notice.commonInfo.etp",
    "data.structuredObject.notice.commonInfo.etp.code",
    "data.structuredObject.notice.commonInfo.href",
    "data.structuredObject.notice.bidderOrg",
    "data.structuredObject.notice.bidderOrg.orgInfo",
    "data.structuredObject.notice.bidderOrg.orgInfo.code",
    "data.structuredObject.notice.bidderOrg.orgInfo.name",
    "data.structuredObject.notice.bidderOrg.orgInfo.INN",
    "data.structuredObject.notice.bidderOrg.orgInfo.KPP",
    "data.structuredObject.notice.bidderOrg.orgInfo.OGRN",
    "data.structuredObject.notice.bidderOrg.orgInfo.orgType",
    "data.structuredObject.notice.bidderOrg.orgInfo.legalAddress",
    "data.structuredObject.notice.bidderOrg.orgInfo.actualAddress",
    "data.structuredObject.notice.bidderOrg.contactInfo",
    "data.structuredObject.notice.bidderOrg.contactInfo.contPerson",
    "data.structuredObject.notice.bidderOrg.contactInfo.tel",
    "data.structuredObject.notice.bidderOrg.contactInfo.email",
    "data.structuredObject.notice.rightHolderInfo",
    "data.structuredObject.notice.rightHolderInfo.biddOrgRightHolder",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.code",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.name",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.INN",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.KPP",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.OGRN",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.orgType",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.legalAddress",
    "data.structuredObject.notice.rightHolderInfo.rightHolderOrg.actualAddress",
    "data.structuredObject.notice.lots",
    "data.structuredObject.notice.lots.lotNumber",
    "data.structuredObject.notice.lots.lotStatus",
    "data.structuredObject.notice.lots.lotName",
    "data.structuredObject.notice.lots.lotDescription",
    "data.structuredObject.notice.lots.priceMin",
    "data.structuredObject.notice.lots.deposit",
    "data.structuredObject.notice.lots.accountsRequisites",
    "data.structuredObject.notice.lots.accountsRequisites.electronicPlatform",
    "data.structuredObject.notice.lots.accountsRequisites.recipient",
    "data.structuredObject.notice.lots.accountsRequisites.recipient.name",
    "data.structuredObject.notice.lots.accountsRequisites.recipient.INN",
    "data.structuredObject.notice.lots.accountsRequisites.recipient.KPP",
    "data.structuredObject.notice.lots.accountsRequisites.bankName",
    "data.structuredObject.notice.lots.accountsRequisites.BIK",
    "data.structuredObject.notice.lots.accountsRequisites.payAccount",
    "data.structuredObject.notice.lots.accountsRequisites.corAccount",
    "data.structuredObject.notice.lots.accountsRequisites.purposePayment",
    "data.structuredObject.notice.lots.currency",
    "data.structuredObject.notice.lots.currency.code",
    "data.structuredObject.notice.lots.privatizationReason",
    "data.structuredObject.notice.lots.biddingObjectInfo",
    "data.structuredObject.notice.lots.biddingObjectInfo.subjectRF",
    "data.structuredObject.notice.lots.biddingObjectInfo.subjectRF.code",
    "data.structuredObject.notice.lots.biddingObjectInfo.estateAddress",
    "data.structuredObject.notice.lots.biddingObjectInfo.estateAddressFIAS",
    "data.structuredObject.notice.lots.category",
    "data.structuredObject.notice.lots.category.code",
    "data.structuredObject.notice.lots.category.name",
    "data.structuredObject.notice.lots.isCompound",
    "data.structuredObject.notice.lots.ownershipForms",
    "data.structuredObject.notice.lots.ownershipForms.code",
    "data.structuredObject.notice.lots.ownershipForms.name",
    "data.structuredObject.notice.lots.characteristics",
    "data.structuredObject.notice.lots.characteristics.code",
    "data.structuredObject.notice.lots.characteristics.name",
    "data.structuredObject.notice.lots.characteristics.characteristicValue",
    "data.structuredObject.notice.lots.characteristics.characteristicValue.code",
    "data.structuredObject.notice.lots.characteristics.characteristicValue.name",
    "data.structuredObject.notice.lots.additionalDetails",
    "data.structuredObject.notice.lots.additionalDetails.code",
    "data.structuredObject.notice.lots.additionalDetails.name",
    "data.structuredObject.notice.lots.additionalDetails.value",
    "data.structuredObject.notice.lots.additionalDetails.imageIds",
    "data.structuredObject.notice.lots.additionalDetails.imageIds.id",
    "data.structuredObject.notice.lots.additionalDetails.imageIds.name",
    "data.structuredObject.notice.lots.additionalDetails.imageIds.size",
    "data.structuredObject.notice.lots.additionalDetails.imageIds.hash",
    "data.structuredObject.notice.lots.additionalDetails.imageIds.attachmentType",
    "data.structuredObject.notice.lots.additionalDetails.imageIds.attachmentType.code",
    "data.structuredObject.notice.biddConditions",
    "data.structuredObject.notice.biddConditions.biddStartTime",
    "data.structuredObject.notice.biddConditions.biddEndTime",
    "data.structuredObject.notice.biddConditions.biddRules",
    "data.structuredObject.notice.timeZone",
    "data.structuredObject.notice.timeZone.code",
    "data.structuredObject.notice.timeZone.name",
    "data.structuredObject.notice.additionalDetails",
    "data.structuredObject.notice.additionalDetails.code",
    "data.structuredObject.notice.additionalDetails.name",
    "data.structuredObject.notice.additionalDetails.value", 
    "data.structuredObject.notice.signedData",
    "data.structuredObject.notice.signedData.fileType",  
    "data.structuredObject.notice.signedData.id", 
    "data.structuredObject.notice.signedData.size", 
    "data.structuredObject.notice.signedData.hash", 
    "data.structuredObject.notice.docs",
    "data.structuredObject.notice.docs.id",
    "data.structuredObject.notice.docs.name",
    "data.structuredObject.notice.docs.size",
    "data.structuredObject.notice.docs.hash",
    "data.structuredObject.notice.docs.attachmentType",
    "data.structuredObject.notice.docs.attachmentType.code",
    "data.structuredObject.notice.docs.attachmentType.name",
    ]

@pytest.fixture(scope="module")
def valid_json():
    json_path = Path(__file__).parent / "notice_25000000390000000060.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_valid_notice(valid_json):
    resp = requests.post(url, json=valid_json, headers=HEADERS, timeout=30)
    assert resp.status_code == 200, f"{resp.status_code}: {resp.text}"
    confirmation = resp.json().get("confirmation", {})
    result = confirmation.get("result")
    assert result == "SUCCESS", (
        f"Невалидный статус: '{result}'. Ожидался SUCCESS"
    )




def remove_attribute(data: dict, path: str) -> None:
    keys = path.split('.')
    current = data
    
    for key in keys[:-1]:
        if isinstance(current, list):
            current = current[0]
        current = current[key]
    last_key = keys[-1]
    if isinstance(current, list):
        current = current[0]
    if last_key in current:
        del current[last_key]



@pytest.mark.parametrize("field_path", REQUIRED)
def test_without_1_required(valid_json, field_path):
    payload = copy.deepcopy(valid_json)
    remove_attribute(payload, field_path)
    resp = requests.post(url, json=payload, headers=HEADERS, timeout=30)
    assert resp.status_code == 422, (
        f"В запросе нет '{field_path}' , но сервер вернул {resp.status_code} вместо 422.\n"
        f"Ответ - {resp.text}")
    confirmation = resp.json().get("confirmation", {})
    result = confirmation.get("result")
    assert result == "FAILURE", (
        f"Невалидный статус: '{result}'. Ожидался FAILURE"
    )
    
