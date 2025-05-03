# API Reference

## Базовая информация

- **Базовый URL**: `http://localhost:8000/api/`
- **Формат данных**: JSON
- **Аутентификация**: Basic Auth, JWT (планируется)

## Endpoints

### Аутентификация

#### Получение токена (планируется)

```
POST /api/token/
```

Параметры запроса:
```json
{
  "username": "string",
  "password": "string"
}
```

Ответ:
```json
{
  "access": "string",
  "refresh": "string"
}
```

### Специалисты

#### Получение списка специалистов

```
GET /api/specialists/
```

Параметры запроса:
- `search`: поиск по имени или специализации
- `ordering`: сортировка (`name`, `-name`, `specialization`, `-specialization`)
- `page`: номер страницы для пагинации
- `page_size`: размер страницы для пагинации

Ответ:
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/specialists/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "doctor1",
        "email": "doctor1@example.com",
        "first_name": "Иван",
        "last_name": "Иванов"
      },
      "name": "Иван Иванов",
      "specialization": "Стоматолог",
      "description": "Опытный стоматолог с 10-летним стажем",
      "photo": "http://localhost:8000/media/specialists/ivan.jpg",
      "is_active": true
    },
    // ... другие специалисты
  ]
}
```

#### Получение информации о конкретном специалисте

```
GET /api/specialists/{id}/
```

Ответ:
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "doctor1",
    "email": "doctor1@example.com",
    "first_name": "Иван",
    "last_name": "Иванов"
  },
  "name": "Иван Иванов",
  "specialization": "Стоматолог",
  "description": "Опытный стоматолог с 10-летним стажем",
  "photo": "http://localhost:8000/media/specialists/ivan.jpg",
  "is_active": true
}
```

#### Получение услуг специалиста

```
GET /api/specialists/{id}/services/
```

Ответ:
```json
[
  {
    "id": 1,
    "name": "Консультация",
    "description": "Первичная консультация",
    "price": "1000.00",
    "duration": 30,
    "specialist": 1,
    "specialist_name": "Иван Иванов",
    "is_active": true
  },
  // ... другие услуги
]
```

#### Получение доступных слотов для записи

```
GET /api/specialists/{id}/available_slots/?date=2024-05-20
```

Параметры запроса:
- `date`: дата в формате YYYY-MM-DD

Ответ:
```json
[
  {
    "start_time": "09:00",
    "end_time": "09:30"
  },
  {
    "start_time": "09:30",
    "end_time": "10:00"
  },
  // ... другие слоты
]
```

### Услуги

#### Получение списка услуг

```
GET /api/services/
```

Параметры запроса:
- `search`: поиск по названию или имени специалиста
- `ordering`: сортировка (`name`, `-name`, `price`, `-price`, `duration`, `-duration`)
- `page`: номер страницы для пагинации
- `page_size`: размер страницы для пагинации

Ответ:
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/services/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Консультация",
      "description": "Первичная консультация",
      "price": "1000.00",
      "duration": 30,
      "specialist": 1,
      "specialist_name": "Иван Иванов",
      "is_active": true
    },
    // ... другие услуги
  ]
}
```

#### Получение информации о конкретной услуге

```
GET /api/services/{id}/
```

Ответ:
```json
{
  "id": 1,
  "name": "Консультация",
  "description": "Первичная консультация",
  "price": "1000.00",
  "duration": 30,
  "specialist": 1,
  "specialist_name": "Иван Иванов",
  "is_active": true
}
```

### Клиенты

#### Получение списка клиентов (только для администраторов)

```
GET /api/clients/
```

Параметры запроса:
- `search`: поиск по имени, телефону или email
- `page`: номер страницы для пагинации
- `page_size`: размер страницы для пагинации

Ответ:
```json
{
  "count": 20,
  "next": "http://localhost:8000/api/clients/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 3,
        "username": "client1",
        "email": "client1@example.com",
        "first_name": "Петр",
        "last_name": "Петров"
      },
      "name": "Петр Петров",
      "phone": "+79123456789",
      "email": "client1@example.com"
    },
    // ... другие клиенты
  ]
}
```

#### Получение информации о клиенте

```
GET /api/clients/{id}/
```

Ответ:
```json
{
  "id": 1,
  "user": {
    "id": 3,
    "username": "client1",
    "email": "client1@example.com",
    "first_name": "Петр",
    "last_name": "Петров"
  },
  "name": "Петр Петров",
  "phone": "+79123456789",
  "email": "client1@example.com"
}
```

#### Создание нового клиента

```
POST /api/clients/
```

Параметры запроса:
```json
{
  "name": "Сергей Сидоров",
  "phone": "+79234567890",
  "email": "sergey@example.com"
}
```

Ответ:
```json
{
  "id": 2,
  "user": {
    "id": 4,
    "username": "client2",
    "email": "sergey@example.com",
    "first_name": "",
    "last_name": ""
  },
  "name": "Сергей Сидоров",
  "phone": "+79234567890",
  "email": "sergey@example.com"
}
```

### Записи

#### Получение списка записей

```
GET /api/appointments/
```

Параметры запроса:
- `search`: поиск по имени клиента, специалиста или услуги
- `ordering`: сортировка (`date`, `-date`, `start_time`, `-start_time`, `status`, `-status`)
- `page`: номер страницы для пагинации
- `page_size`: размер страницы для пагинации

Ответ:
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "client": 1,
      "client_name": "Петр Петров",
      "service": 1,
      "service_name": "Консультация",
      "specialist": 1,
      "specialist_name": "Иван Иванов",
      "date": "2024-05-20",
      "start_time": "10:00:00",
      "end_time": "10:30:00",
      "status": "pending",
      "created_at": "2024-05-15T12:30:45Z",
      "updated_at": "2024-05-15T12:30:45Z"
    },
    // ... другие записи
  ]
}
```

#### Получение информации о конкретной записи

```
GET /api/appointments/{id}/
```

Ответ:
```json
{
  "id": 1,
  "client": 1,
  "client_name": "Петр Петров",
  "service": 1,
  "service_name": "Консультация",
  "specialist": 1,
  "specialist_name": "Иван Иванов",
  "date": "2024-05-20",
  "start_time": "10:00:00",
  "end_time": "10:30:00",
  "status": "pending",
  "created_at": "2024-05-15T12:30:45Z",
  "updated_at": "2024-05-15T12:30:45Z"
}
```

#### Создание новой записи

```
POST /api/appointments/
```

Параметры запроса:
```json
{
  "client": 1,
  "service": 1,
  "specialist": 1,
  "date": "2024-05-21",
  "start_time": "11:00:00",
  "end_time": "11:30:00"
}
```

Ответ:
```json
{
  "id": 2,
  "client": 1,
  "client_name": "Петр Петров",
  "service": 1,
  "service_name": "Консультация",
  "specialist": 1,
  "specialist_name": "Иван Иванов",
  "date": "2024-05-21",
  "start_time": "11:00:00",
  "end_time": "11:30:00",
  "status": "pending",
  "created_at": "2024-05-15T14:20:10Z",
  "updated_at": "2024-05-15T14:20:10Z"
}
```

#### Отмена записи

```
POST /api/appointments/{id}/cancel/
```

Ответ:
```json
{
  "id": 1,
  "client": 1,
  "client_name": "Петр Петров",
  "service": 1,
  "service_name": "Консультация",
  "specialist": 1,
  "specialist_name": "Иван Иванов",
  "date": "2024-05-20",
  "start_time": "10:00:00",
  "end_time": "10:30:00",
  "status": "cancelled",
  "created_at": "2024-05-15T12:30:45Z",
  "updated_at": "2024-05-15T14:25:30Z"
}
```

#### Подтверждение записи

```
POST /api/appointments/{id}/confirm/
```

Ответ:
```json
{
  "id": 2,
  "client": 1,
  "client_name": "Петр Петров",
  "service": 1,
  "service_name": "Консультация",
  "specialist": 1,
  "specialist_name": "Иван Иванов",
  "date": "2024-05-21",
  "start_time": "11:00:00",
  "end_time": "11:30:00",
  "status": "confirmed",
  "created_at": "2024-05-15T14:20:10Z",
  "updated_at": "2024-05-15T14:26:15Z"
}
```

#### Завершение записи

```
POST /api/appointments/{id}/complete/
```

Ответ:
```json
{
  "id": 2,
  "client": 1,
  "client_name": "Петр Петров",
  "service": 1,
  "service_name": "Консультация",
  "specialist": 1,
  "specialist_name": "Иван Иванов",
  "date": "2024-05-21",
  "start_time": "11:00:00",
  "end_time": "11:30:00",
  "status": "completed",
  "created_at": "2024-05-15T14:20:10Z",
  "updated_at": "2024-05-21T11:40:00Z"
}
```

## Коды ошибок

- **400 Bad Request**: Неверные параметры запроса
- **401 Unauthorized**: Требуется аутентификация
- **403 Forbidden**: Недостаточно прав для выполнения операции
- **404 Not Found**: Запрашиваемый ресурс не найден
- **500 Internal Server Error**: Внутренняя ошибка сервера

## Пример использования API с Python

```python
import requests
from requests.auth import HTTPBasicAuth

# Базовый URL
BASE_URL = 'http://localhost:8000/api'

# Аутентификация
username = 'admin'
password = 'admin123'
auth = HTTPBasicAuth(username, password)

# Получение списка специалистов
response = requests.get(f'{BASE_URL}/specialists/', auth=auth)
specialists = response.json()

# Получение списка услуг специалиста
specialist_id = specialists['results'][0]['id']
response = requests.get(f'{BASE_URL}/specialists/{specialist_id}/services/', auth=auth)
services = response.json()

# Получение доступных слотов
date = '2024-05-20'
response = requests.get(f'{BASE_URL}/specialists/{specialist_id}/available_slots/?date={date}', auth=auth)
slots = response.json()

# Создание записи
client_id = 1
service_id = services[0]['id']
appointment_data = {
    'client': client_id,
    'service': service_id,
    'specialist': specialist_id,
    'date': date,
    'start_time': slots[0]['start_time'],
    'end_time': slots[0]['end_time']
}
response = requests.post(f'{BASE_URL}/appointments/', json=appointment_data, auth=auth)
appointment = response.json()

# Подтверждение записи
appointment_id = appointment['id']
response = requests.post(f'{BASE_URL}/appointments/{appointment_id}/confirm/', auth=auth)
``` 