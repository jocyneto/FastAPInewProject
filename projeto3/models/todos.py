from pydantic import BaseModel, Field
from typing import Optional


class Todos_Model(BaseModel):
    """
    title, descritption, priority, complete
    """
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool
