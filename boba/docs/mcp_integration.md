# Интеграция с MCP (Model Context Protocol)

## Обзор

Model Context Protocol (MCP) - это протокол для взаимодействия с языковыми моделями, позволяющий создавать контекстно-зависимые взаимодействия с пользователями. В нашем проекте MCP будет использоваться для создания ИИ-ассистента, способного понимать естественный язык пользователей и выполнять действия через API.

## Архитектура

```
+---------------+     +---------------+     +---------------+
|               |     |               |     |               |
| Telegram Bot  | <-> |  MCP Server   | <-> |  Django API   |
|               |     |               |     |               |
+---------------+     +---------------+     +---------------+
```

## Компоненты MCP-интеграции

### 1. Функции (Functions)

Функции - это методы, которые MCP может вызывать для взаимодействия с API. Каждая функция соответствует определенной операции с API.

Пример функций:

```python
def get_specialists():
    """Получить список активных специалистов"""
    response = requests.get(f"{API_URL}/specialists/")
    return response.json()

def get_specialist_services(specialist_id):
    """Получить услуги специалиста"""
    response = requests.get(f"{API_URL}/specialists/{specialist_id}/services/")
    return response.json()

def get_available_slots(specialist_id, date):
    """Получить доступные слоты для записи"""
    response = requests.get(f"{API_URL}/specialists/{specialist_id}/available_slots/?date={date}")
    return response.json()

def create_appointment(client_id, specialist_id, service_id, date, start_time, end_time):
    """Создать запись на прием"""
    data = {
        "client": client_id,
        "specialist": specialist_id,
        "service": service_id,
        "date": date,
        "start_time": start_time,
        "end_time": end_time
    }
    response = requests.post(f"{API_URL}/appointments/", json=data)
    return response.json()
```

### 2. Контекст (Context)

Контекст - это информация о текущем состоянии разговора с пользователем. Контекст помогает MCP понимать предыдущие взаимодействия и поддерживать непрерывность разговора.

Пример структуры контекста:

```json
{
  "user_id": "12345",
  "username": "john_doe",
  "current_flow": "booking",
  "selected_specialist": 1,
  "selected_service": 3,
  "selected_date": "2024-05-20",
  "selected_time_slot": "14:00-14:30",
  "previous_appointments": [
    {
      "id": 42,
      "service": "Консультация",
      "date": "2024-04-15",
      "status": "completed"
    }
  ]
}
```

### 3. Интенты (Intents)

Интенты - это намерения пользователя, которые MCP должен распознать из естественного языка.

Примеры интентов:
- `find_specialist` - поиск специалиста
- `list_services` - просмотр услуг
- `book_appointment` - запись на прием
- `cancel_appointment` - отмена записи
- `reschedule_appointment` - перенос записи

## Примеры взаимодействия с MCP

### Сценарий 1: Запись к специалисту

Пользователь: "Хочу записаться к стоматологу"

1. MCP распознает интент `find_specialist` с параметром `specialization="стоматолог"`
2. MCP вызывает функцию `get_specialists(specialization="стоматолог")`
3. MCP получает список стоматологов и предлагает пользователю выбрать
4. Пользователь: "Выбираю доктора Иванова"
5. MCP обновляет контекст: `selected_specialist=1`
6. MCP вызывает функцию `get_specialist_services(specialist_id=1)`
7. MCP получает список услуг и предлагает пользователю выбрать
8. Пользователь: "Мне нужна консультация"
9. MCP обновляет контекст: `selected_service=3`
10. MCP вызывает функцию `get_available_slots(specialist_id=1, date="2024-05-20")`
11. MCP получает список доступных слотов и предлагает пользователю выбрать
12. Пользователь: "Запишите меня на 14:00"
13. MCP обновляет контекст: `selected_time_slot="14:00-14:30"`
14. MCP вызывает функцию `create_appointment(...)`
15. MCP подтверждает запись и предоставляет пользователю детали

## Схема интеграции с Django API

Для интеграции MCP с Django API необходимо:

1. Создать MCP-сервер, который будет обрабатывать запросы от Telegram Bot
2. Реализовать функции для взаимодействия с Django API
3. Определить интенты и обработчики для них
4. Реализовать хранение и обновление контекста разговора
5. Создать Telegram Bot, который будет взаимодействовать с MCP-сервером

## Следующие шаги

1. Установка и настройка MCP SDK
2. Определение и реализация функций для взаимодействия с API
3. Определение интентов и сценариев взаимодействия
4. Интеграция с Telegram Bot API
5. Тестирование и отладка 