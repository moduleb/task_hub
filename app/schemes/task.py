"""
Создаем модели данных для валидации pydantic
"""

from typing import Optional, List

from pydantic import BaseModel, Field

PATTERN = r'^[a-zA-Zа-яА-Я0-9 _]+$'

class TaskValidation(BaseModel):
    """
    Схема валидации при создании и обновлении.
    """
    taskname: str = Field(
        min_length=3, max_length=100, pattern=PATTERN,
        examples=['Task 1', 'Student Work 15'])
    description: Optional[str] = Field(
        default=None, max_length=500, pattern=PATTERN,
        examples=['Draw a picture', 'Do homework'])
    category: Optional[str] = Field(
        default=None, max_length=100, pattern=PATTERN,
        examples=['Hobby', 'Study'])


class TaskView(BaseModel):
    """
    Схема отображения задания.
    """
    id: int = Field(examples=[1])
    taskname: str = Field(examples=['Task 1', 'Student Work 15'])
    description: str = Field(examples=['Draw a picture', 'Do homework'], default=None)
    category: str = Field(examples=['Hobby', 'Study'], default=None)
    creation_date: str = Field(examples=["2023-12-11T19:35:46"])

class TasksListResponse(BaseModel):
    data: List[TaskView]

class TaskResponse(BaseModel):
    data: TaskView

class ErrorMessage(BaseModel):
    detail: str = Field(examples=['Error description'])

class SuccessMessage(BaseModel):
    detail: str = Field(examples=['Success message'])


