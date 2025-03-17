"""
Модуль для панели управления FastAPI
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from database import AttendanceDatabase
from bot import VkBot

from config.config import ADMINS, update_config


app = FastAPI()
db = AttendanceDatabase()
vk_bot = VkBot(db=db)


#TODO: переместить в контракты
class ConfigUpdate(BaseModel):
    vk_token: str = Field(
        title="Токен для бота ВКонтакте",
        default="vk1.a.fZnFDaMgklg5QhCrUZ2kEwkEksR32ZQ4FWg-5mEvzZbFN2Q-k1D-HA6ioVOTvUw7Pyz_B25cw9ezloK3tmobWizeuhuaYsaxnZ8JL3Gs5k-E5ApXFtAcsxw-BzoJo6710kYE0Tte4GxQVaFZTbhjr-KmQeh_P9JQeIeEKmtdJbPA4_MZxxHtXAkeW2IjNBCjSj_MZe7s5038sW2f_3lpmg"
    )
    group_id: Optional[int] = Field(
        title="ID группы ВКонтакте для бота",
        default=186471220
    )
    admins: Optional[list[int]] = Field(
        title="Список ID VK администраторов",
        default=[286001249]
        )
    chat_id: Optional[int] = Field(
        title="ID чата флуда",
        default=2
        )
    chat_id_kick: Optional[int] = Field(
        title="ID информационного чата",
        default=3
        )
    percent: Optional[int] = Field(
        title="Пограничный процент посещаемости за последние 5 тренировок (от 0 до 100)",
        default=20
        )
    google_sheet_name: Optional[str] = Field(
        title="Наименование таблицы Google Sheets",
        default="Радиус Журнал"
        )
    google_credentials_path: Optional[str] = Field(
        title="Путь до json-файла с данными авторизации в Google"
        )
    

@app.post("/attendance")
async def attendance_record():
    #TODO: реализовать с await
    pass

@app.post("/money")
async def money_record():
    #TODO: реализовать с await
    pass

@app.post("/illegal")
async def illegal_kick():
    #TODO: реализовать
    pass

@app.post("/kick")
async def day_of_kick():
    #TODO: реализовать
    pass

#TODO: пересмотреть необходимость
@app.get("/stats")
async def get_stats():
    """
    Эндпоинт для получения статистики посещаемости из локальной БД
    """
    stats = db.cursor.execute("SELECT user_id, username, COUNT(*) FROM attendance GROUP BY user_id").fetchall()
    return {"attendance": stats}

@app.delete("/remove_user/{user_id}")
async def remove_user(user_id: int):
    """
    Эндпоинт для удаления пользователя из локальной БД и чата ВК
    """
    if user_id not in ADMINS:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления пользователя")
    
    db.remove_user(user_id)
    response = vk_bot.remove_user_from_chat(user_id)
    
    if "error" in response:
        raise HTTPException(status_code=400, detail=f"Ошибка VK API: {response['error']['error_msg']}")

    return {"message": f"Пользователь {user_id} удалён."}

#TODO: пересмотреть реализацию (исключения?)
@app.put("/update_config")
async def update_config(config_new: ConfigUpdate):
    """
    Эндпоинт для обновления конфигурационных данных
    """
    try:
        update_config(config_new.model_dump())
        return {"message": "Конфигурационный файл добавлен успешно"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))