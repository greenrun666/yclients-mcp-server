# YCLIENTS MCP Server

MCP-сервер для полного доступа к [YCLIENTS REST API](https://developer.yclients.com/). Позволяет AI-агентам (включая агентов Timeweb Cloud) взаимодействовать с платформой YCLIENTS.

## 🚀 Возможности

- **30+ инструментов** для работы с YCLIENTS API
- **Совместимость с Timeweb Cloud AI Agents** (Streamable HTTP транспорт)
- **Rate limiting** (5 req/s, 200 req/min) для соблюдения лимитов API
- **Поддержка stdio и HTTP** транспортов

## 📦 Инструменты

### Компании
- `yclients_get_companies` - Получить список компаний
- `yclients_get_company` - Получить информацию о компании
- `yclients_create_company` - Создать компанию
- `yclients_update_company` - Обновить компанию

### Услуги
- `yclients_get_services` - Получить список услуг
- `yclients_get_service` - Получить информацию об услуге
- `yclients_create_service` - Создать услугу
- `yclients_get_service_categories` - Получить категории услуг
- `yclients_create_service_category` - Создать категорию услуг

### Сотрудники
- `yclients_get_staff` - Получить список сотрудников
- `yclients_get_staff_member` - Получить информацию о сотруднике
- `yclients_create_staff` - Создать сотрудника
- `yclients_update_staff` - Обновить сотрудника
- `yclients_delete_staff` - Удалить сотрудника
- `yclients_get_positions` - Получить список должностей

### Клиенты
- `yclients_search_clients` - Поиск клиентов
- `yclients_get_client` - Получить информацию о клиенте
- `yclients_create_client` - Создать клиента
- `yclients_update_client` - Обновить клиента
- `yclients_delete_client` - Удалить клиента
- `yclients_get_client_visits` - История посещений клиента

### Записи
- `yclients_get_records` - Получить список записей
- `yclients_get_record` - Получить информацию о записи
- `yclients_create_record` - Создать запись
- `yclients_update_record` - Обновить запись
- `yclients_delete_record` - Удалить запись

### Онлайн-запись
- `yclients_get_booking_settings` - Настройки формы бронирования
- `yclients_get_available_dates` - Доступные даты
- `yclients_get_available_times` - Доступные слоты времени
- `yclients_get_available_staff` - Доступные сотрудники
- `yclients_get_available_services` - Доступные услуги
- `yclients_create_booking` - Создать онлайн-запись
- `yclients_get_nearest_available` - Ближайшие доступные слоты

### Расписание
- `yclients_get_schedule` - Получить расписание
- `yclients_get_timetable` - Детальное расписание сотрудника
- `yclients_get_workload` - Загруженность сотрудников

### Аналитика
- `yclients_get_company_stats` - Основные показатели
- `yclients_get_revenue_by_day` - Выручка по дням
- `yclients_get_records_by_day` - Записи по дням
- `yclients_get_occupancy_by_day` - Заполненность по дням
- `yclients_get_records_by_source` - Записи по источникам
- `yclients_get_records_by_status` - Записи по статусам
- `yclients_get_z_report` - Z-отчет

## 🛠 Установка

### Требования
- Python 3.10+
- Partner-токен YCLIENTS ([получить в Маркетплейсе](https://yclients.com/appstore/developers))

### Локальная установка

```bash
git clone https://github.com/YOUR_USERNAME/yclients-mcp-server.git
cd yclients-mcp-server

# Используя uv (рекомендуется)
uv sync

# Или pip
pip install -e .
```

### Переменные окружения

```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваши токены
```

## 🚀 Запуск

### Локально (stdio)

```bash
YCLIENTS_PARTNER_TOKEN=... MCP_TRANSPORT=stdio python -m yclients_mcp.server
```

### HTTP сервер (для Timeweb)

```bash
YCLIENTS_PARTNER_TOKEN=... MCP_TRANSPORT=http python -m yclients_mcp.server
```

Сервер будет доступен на `http://localhost:8000/mcp`

### Docker

```bash
docker build -t yclients-mcp-server .
docker run -p 8000:8000 \
  -e YCLIENTS_PARTNER_TOKEN=your_token \
  -e YCLIENTS_USER_TOKEN=your_user_token \
  yclients-mcp-server
```

## 🔗 Подключение к Timeweb Cloud AI Agents

1. Разверните сервер на Timeweb Cloud (App Platform или Cloud Server)
2. В панели управления Timeweb перейдите в **AI-агенты → MCP-серверы**
3. Нажмите **Добавить** и заполните:
   - **Название**: YCLIENTS
   - **Адрес сервера**: `https://your-server.timeweb.cloud/mcp`
   - **Протокол**: HTTP
   - **Авторизация**: Без авторизации (или Bearer-токен если настроили)
4. Подключите MCP-сервер к вашему AI-агенту

## 📋 Пример использования

После подключения к AI-агенту Timeweb, вы можете использовать естественный язык:

> "Покажи список моих компаний в YCLIENTS"

> "Создай запись для клиента Иван Петров на стрижку завтра в 14:00"

> "Какая выручка была за последнюю неделю?"

## 🔒 Безопасность

- **Никогда** не храните токены в коде
- Используйте переменные окружения или секреты
- Для production используйте HTTPS

## 📄 Лицензия

MIT

## 🤝 Вклад

Pull requests приветствуются! Для крупных изменений сначала откройте issue.
