test_integretions/
├── conftest.py                       # Конфигурация
├── test_rosim_notice_integration.py  # Тесты
├── schemas/
│   ├── Notice.json                   # (АТФФ 5.1)
│   ├── base.json                     # Зависимости схемы
│   └── https_packet_schema.json      # Схема транспортного пакета
├── fixtures/
│   ├── valid_notice.json             # Валидный JSON от Росимущества
│   ├── patches/                      # Патчи для негативных тестов
│   └── files/                        # Тестовые файлы для ФХ
├── utils/
│   ├── signature_helper.py           # Генерация подписи (CadES-BES)
│   └── file_storage_client.py        # Клиент для ФХ ГИС Торги