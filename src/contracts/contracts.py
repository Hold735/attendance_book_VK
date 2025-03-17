"""
Модуль с описанием контрактов
"""
from pydantic import BaseModel


class Message(BaseModel):
    pass

class MarkVisit(Message):
    pass
