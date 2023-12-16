"""
Создаем модели данных для валидации pydantic
"""

from typing import Optional

from pydantic import BaseModel, Field

PATTERN = r'^[a-zA-Zа-яА-Я0-9 _]+$'

class TaskDTO(BaseModel):
    """
    Схема входных данных от пользователя
    """
    taskname: str = Field(min_length=3, max_length=100, pattern=PATTERN)
    description: Optional[str] = Field(None, max_length=500, pattern=PATTERN)
    category: Optional[str] = Field(None, max_length=100, pattern=PATTERN)
    # datetime: Optional[datetime] = Field(gt_datetime=datetime.now())

class Message(BaseModel):
    detail: str
