from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field 

class Book(BaseModel):
    """
    id, title, author, description, rating
    """
    id: Optional[int] = Field(description="No needed input value.", default=None) 
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(ge=1900, le=datetime.now().year)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "Author of a book",
                "description": "A Description of a book util 100 character",
                "rating": 5,
                "published_date": 2024
            }
        }
    }
