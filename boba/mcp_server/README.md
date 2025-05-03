# MCP Server для Booking Assistant

Model Context Protocol (MCP) сервер для интеграции Django API с Telegram ботом.

## Структура

```
mcp_server/
├── functions/           # Функции для взаимодействия с API
│   ├── appointments.py  # Работа с записями
│   ├── clients.py       # Работа с клиентами
│   ├── services.py      # Работа с услугами
│   └── specialists.py   # Работа со специалистами
├── intents/             # Обработчики намерений пользователя
│   ├── booking.py       # Запись на прием
│   ├── cancellation.py  # Отмена записи
│   ├── information.py   # Информация об услугах и специалистах
│   └── registration.py  # Регистрация клиентов
├── api_client.py        # Клиент для взаимодействия с API
├── context.py           # Управление контекстом диалога
├── main.py              # Основной модуль сервера
└── utils.py             # Вспомогательные функции
```

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения:
```bash
export API_URL=http://localhost:8000/api
export API_USERNAME=admin
export API_PASSWORD=admin123
export MCP_SERVER_PORT=5000
```

3. Запустите сервер:
```bash
python main.py
```

## API

MCP-сервер предоставляет следующие эндпоинты:

### Обработка сообщений

```
POST /process
```

Параметры запроса:
```json
{
  "user_id": "string",
  "message": "string",
  "context": {
    "key": "value"
  }
}
```

Ответ:
```json
{
  "response": "string",
  "context": {
    "key": "value"
  },
  "actions": [
    {
      "type": "string",
      "payload": {}
    }
  ]
}
```

### Функции

```
GET /functions
```

Возвращает список доступных функций с их описанием и параметрами.

### Интенты

```
GET /intents
```

Возвращает список поддерживаемых намерений пользователя. 