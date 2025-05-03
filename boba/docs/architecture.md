# Архитектура проекта Booking Assistant

## Общая схема

```
+----------------+     +----------------+     +----------------+     +----------------+
|                |     |                |     |                |     |                |
| Telegram Bot   | <-> | MCP Server     | <-> | Django API     | <-> | Database       |
|                |     |                |     |                |     |                |
+----------------+     +----------------+     +----------------+     +----------------+
```

## Компоненты

### 1. Django API

Основной бэкенд-сервис, предоставляющий RESTful API для работы с данными. Включает следующие компоненты:

- **Models** - модели данных (Specialist, Service, Client, Appointment)
- **Serializers** - сериализаторы для конвертации моделей в JSON и обратно
- **Views** - представления для обработки запросов
- **URLs** - маршрутизация URL
- **Authentication** - аутентификация и авторизация

### 2. MCP Server

Промежуточный сервер, реализующий Model Context Protocol для взаимодействия с ИИ-моделями:

- **MCP Functions** - функции для взаимодействия с API
- **Context Management** - управление контекстом диалога
- **Intent Recognition** - распознавание намерений пользователя
- **Response Generation** - генерация ответов пользователю
- **API Client** - клиент для взаимодействия с Django API

### 3. Telegram Bot

Фронтенд-клиент для взаимодействия с пользователями через Telegram:

- **Bot Handler** - обработчик сообщений от пользователей
- **MCP Client** - клиент для взаимодействия с MCP Server
- **UI Components** - компоненты пользовательского интерфейса (кнопки, меню и т.д.)

### 4. Database

База данных для хранения информации:

- **Django Models** - таблицы и связи, определенные через модели Django
- **Context Storage** - хранение контекста диалогов для MCP
- **User Sessions** - хранение сессий пользователей

## Потоки данных

### 1. Регистрация и авторизация

```
Клиент -> Telegram Bot -> MCP Server -> Django API -> Database
```

### 2. Поиск специалиста и услуги

```
Клиент -> Telegram Bot -> MCP Server -> Django API -> Database
                       <- MCP Server <- Django API
Клиент <- Telegram Bot <- MCP Server (генерация ответа)
```

### 3. Запись на прием

```
Клиент -> Telegram Bot -> MCP Server (распознавание интента)
                       -> Django API (проверка доступности)
                       -> Django API (создание записи)
                       -> Database (сохранение)
Клиент <- Telegram Bot <- MCP Server (подтверждение)
```

### 4. Управление записями

```
Клиент -> Telegram Bot -> MCP Server -> Django API -> Database
                                     <- Django API
Клиент <- Telegram Bot <- MCP Server
```

## Технологический стек

### Backend
- **Django**: веб-фреймворк для API
- **Django REST Framework**: создание RESTful API
- **SQLite/PostgreSQL**: база данных
- **Python**: основной язык программирования

### MCP Server
- **Python**: язык программирования
- **MCP SDK**: библиотека для работы с Model Context Protocol
- **requests**: HTTP-клиент для взаимодействия с API

### Frontend (Telegram Bot)
- **Python**: язык программирования
- **python-telegram-bot**: библиотека для создания Telegram бота
- **aiohttp**: асинхронный HTTP-клиент для взаимодействия с MCP Server

## Безопасность

- **JWT Authentication**: для API
- **Telegram API Authentication**: для Telegram Bot
- **HTTPS**: для всех сетевых взаимодействий
- **Data Encryption**: для чувствительных данных

## Масштабирование

- **Stateless API**: возможность горизонтального масштабирования API
- **Caching**: кэширование часто запрашиваемых данных
- **Task Queues**: для обработки асинхронных задач

## Тестирование

- **Unit Tests**: тестирование отдельных компонентов
- **Integration Tests**: тестирование взаимодействия компонентов
- **E2E Tests**: тестирование полного взаимодействия от пользователя до базы данных
- **Mock Services**: для изоляции компонентов при тестировании 