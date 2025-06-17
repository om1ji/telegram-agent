#!/usr/bin/env python3
from datetime import datetime
import httpx
from mcp.server.fastmcp import FastMCP
from asyncio import run

API_BASE_URL = "http://localhost:8000/api"
AUTH_TOKEN = "your_auth_token_here"
MCP_BASE_URL = "http://localhost:8080"

DEFAULT_HEADERS = {
    "Authorization": f"Token {AUTH_TOKEN}",
    "Content-Type": "application/json",
}

mcp = FastMCP("Healthcare Booking Assistant")

async def api_get(endpoint, params=None):
    url = f"{API_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=DEFAULT_HEADERS)
        response.raise_for_status()
        return response.json()

async def api_post(endpoint, data):
    url = f"{API_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=DEFAULT_HEADERS)
        response.raise_for_status()
        return response.json()

async def api_patch(endpoint, data):
    url = f"{API_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=data, headers=DEFAULT_HEADERS)
        response.raise_for_status()
        return response.json()

async def api_delete(endpoint):
    url = f"{API_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=DEFAULT_HEADERS)
        response.raise_for_status()
        return response.status_code

@mcp.tool()
async def search_specialists(specialization: str = None, city: str = None, category_id: int = None) -> list:
    """
    Поиск специалистов (врачей) по заданным критериям
    
    Args:
        specialization: Специализация врача (например, "Стоматолог", "Терапевт")
        city: Город, где принимает врач (например, "Казань")
        category_id: ID категории услуг
        
    Returns:
        Список специалистов, соответствующих критериям поиска
    """
    params = {}
    if specialization:
        params["search"] = specialization
    if city:
        params["city"] = city
    if category_id:
        params["category_id"] = category_id
        
    specialists = await api_get("specialists", params)
    return specialists

@mcp.tool()
async def create_appointment(
    specialist_id: int,
    service_id: int,
    client_id: int,
    date: str,
    start_time: str
) -> dict:
    """
    Создать запись на приём к специалисту
    
    Args:
        specialist_id: ID специалиста
        service_id: ID услуги
        client_id: ID клиента
        date: Дата приёма в формате YYYY-MM-DD
        start_time: Время начала приёма в формате HH:MM
        
    Returns:
        Данные созданной записи
    """
    # Получаем услугу для определения продолжительности
    service = await api_get(f"services/{service_id}")
    
    # Расчет времени окончания приема
    duration_minutes = service["duration"]
    
    # Парсим время начала
    hour, minute = map(int, start_time.split(":"))
    
    # Вычисляем время окончания
    end_hour = hour + (minute + duration_minutes) // 60
    end_minute = (minute + duration_minutes) % 60
    end_time = f"{end_hour:02d}:{end_minute:02d}"
    
    appointment_data = {
        "specialist": specialist_id,
        "service": service_id,
        "client": client_id,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "status": "pending"
    }
    
    result = await api_post("appointments", appointment_data)
    return result

@mcp.tool()
async def cancel_appointment(appointment_id: int) -> dict:
    """
    Отменить запись на приём
    
    Args:
        appointment_id: ID записи на приём
        
    Returns:
        Обновленные данные записи
    """
    result = await api_post(f"appointments/{appointment_id}/cancel", {})
    return result

@mcp.tool()
async def confirm_appointment(appointment_id: int) -> dict:
    """
    Подтвердить запись на приём
    
    Args:
        appointment_id: ID записи на приём
        
    Returns:
        Обновленные данные записи
    """
    result = await api_post(f"appointments/{appointment_id}/confirm", {})
    return result

@mcp.tool()
async def complete_appointment(appointment_id: int) -> dict:
    """
    Отметить запись на приём как завершенную
    
    Args:
        appointment_id: ID записи на приём
        
    Returns:
        Обновленные данные записи
    """
    result = await api_post(f"appointments/{appointment_id}/complete", {})
    return result

@mcp.tool()
async def get_available_slots(specialist_id: int, date: str = None) -> list:
    """
    Получить доступные слоты для записи к специалисту на определенную дату
    
    Args:
        specialist_id: ID специалиста
        date: Дата в формате YYYY-MM-DD (если не указана, используется текущая дата)
        
    Returns:
        Список доступных временных слотов
    """
    params = {}
    if date:
        params["date"] = date
    else:
        params["date"] = datetime.now().strftime("%Y-%m-%d")
        
    slots = await api_get(f"specialists/{specialist_id}/available_slots", params)
    return slots

# === RESOURCES ===

@mcp.resource(f"{MCP_BASE_URL}/specialists")
async def get_specialists() -> list:
    """
    Получить список всех специалистов
    """
    return await api_get("specialists")

@mcp.resource(f"{MCP_BASE_URL}/specialists/{{specialist_id}}")
async def get_specialist(specialist_id: int) -> dict:
    """
    Получить информацию о конкретном специалисте
    """
    return await api_get(f"specialists/{specialist_id}")

@mcp.resource(f"{MCP_BASE_URL}/specialists/{{specialist_id}}/services")
async def get_specialist_services(specialist_id: int) -> list:
    """
    Получить список услуг, предоставляемых специалистом
    """
    return await api_get(f"specialists/{specialist_id}/services")

@mcp.resource(f"{MCP_BASE_URL}/specialists/{{specialist_id}}/schedule")
async def get_specialist_schedule(specialist_id: int) -> list:
    """
    Получить расписание работы специалиста
    """
    return await api_get(f"specialists/{specialist_id}/schedule")

@mcp.resource(f"{MCP_BASE_URL}/services")
async def get_services() -> list:
    """
    Получить список всех услуг
    """
    return await api_get("services")

@mcp.resource(f"{MCP_BASE_URL}/services/{{service_id}}")
async def get_service(service_id: int) -> dict:
    """
    Получить информацию о конкретной услуге
    """
    return await api_get(f"services/{service_id}")

@mcp.resource(f"{MCP_BASE_URL}/categories")
async def get_categories() -> list:
    """
    Получить список всех категорий услуг
    """
    return await api_get("categories")

@mcp.resource(f"{MCP_BASE_URL}/categories/{{category_id}}")
async def get_category(category_id: int) -> dict:
    """
    Получить информацию о конкретной категории услуг
    """
    return await api_get(f"categories/{category_id}")

@mcp.resource(f"{MCP_BASE_URL}/appointments")
async def get_appointments() -> list:
    """
    Получить список всех записей на приём
    """
    return await api_get("appointments")

@mcp.resource(f"{MCP_BASE_URL}/appointments/{{appointment_id}}")
async def get_appointment(appointment_id: int) -> dict:
    """
    Получить информацию о конкретной записи на приём
    """
    return await api_get(f"appointments/{appointment_id}")

@mcp.resource(f"{MCP_BASE_URL}/clients")
async def get_clients() -> list:
    """
    Получить список всех клиентов
    """
    return await api_get("clients")

@mcp.resource(f"{MCP_BASE_URL}/clients/{{client_id}}")
async def get_client(client_id: int) -> dict:
    """
    Получить информацию о конкретном клиенте
    """
    return await api_get(f"clients/{client_id}")

if __name__ == "__main__":
    run(mcp.run_stdio_async())