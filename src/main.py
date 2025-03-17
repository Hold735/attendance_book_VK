"""
Конструктор приложения
"""
#TODO: пересмотреть реализацию точки входа
import asyncio
import uvicorn

from database import AttendanceDatabase
from bot import VkBot
from sync import GoogleSync
from api import app

# Создаем и инициализируем объекты для работы с компонентами
db = AttendanceDatabase(db_path="data/attendance.db")
vk_bot = VkBot(db=db)
google_sync = GoogleSync(db=db)

# Основная асинхронная функция для запуска всего
async def start_services():
    # Запуск сервиса для получения сообщений ВКонтакте
    vk_bot.run_polling()

    #TODO: проверить асинхронную работу
    # Синхронизация данных с Google Sheets (по расписанию или вручную)
    await google_sync.sync_data()

# Точка входа для FastAPI сервера
def start_fastapi():
    """Запуск FastAPI сервера для панели управления."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Запуск всех сервисов одновременно
def run():
    """Запускает все сервисы: VK-бот, FastAPI и синхронизацию с Google Sheets."""
    loop = asyncio.get_event_loop()

    # Запуск панели управления (FastAPI) в отдельном потоке
    loop.run_in_executor(None, start_fastapi)

    # Запуск асинхронных сервисов: бота и синхронизации
    loop.run_until_complete(start_services())

if __name__ == "__main__":
    run()
