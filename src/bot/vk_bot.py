"""
Модуль для работы бота ВКонтакте
"""
from vkbottle.bot import Bot, Message

from database import AttendanceDatabase
from config.config import VK_TOKEN, CHAT_ID, CHAT_ID_KICK

bot = Bot(token=VK_TOKEN)


class VkBot:
    """
    Класс реализует методы для управления ботом Вконтакте
    """
    def __init__(
        self,
        db: AttendanceDatabase
    ) -> None:
        """
        Инициализация бота ВКонтакте по токену
        
        :param db: объект локальной БД
        """
        self.token = VK_TOKEN
        self.chat_id = CHAT_ID
        self.chat_id_kick = CHAT_ID_KICK
        self.db = db
        self.bot = Bot(token=self.token)
    
    async def send_message(self, chat_id: int, answer: str):
        await self.bot.api.messages.send(
            peer_id=2000000000 + chat_id,
            message=answer
        )
        
    async def send_answer(self, message: Message, answer: str):
        await message.answer(answer)
        
    
    #TODO: восстановить логику обработки сообщений из легаси кода, написать несколько хендлеров
    async def handle_message(self, message: Message):
        """
        """
        text = message.text
        if len(text) >= 3 and text[:3] == "+++":
            self.db.add_attendance(message.from_id, message.from_id, message.date)
            await message.answer("✅ Отметка о посещении добавлена!")
    
    #TODO: реализовать методику удаления пользователя из чата
    def remove_user_from_chat(self, user_id):
        """
        
        """
        pass
    
    #TODO: реализовать методику получения списка участников чата
    def foo():
        pass
    
    