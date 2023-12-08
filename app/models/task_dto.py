from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

pattern = r'^[a-zA-Zа-яА-Я0-9 _]+$'

class TaskDTO(BaseModel):
    taskname: str = Field(min_length=3, max_length=100, pattern=pattern)
    description: Optional[str] = Field(None, max_length=500, pattern=pattern)
    category: Optional[str] = Field(None, max_length=100, pattern=pattern)
    # datetime: Optional[datetime] = Field(gt_datetime=datetime.now())


"""
- `gt` (greater than) и `lt` (less than): Ограничение числовых полей, например,
    чтобы значение было больше или меньше определенного числа.
- `gt_datetime` и `lt_datetime`: Ограничение полей даты и времени,
    чтобы значение было после или до определенной даты и времени.
"""
