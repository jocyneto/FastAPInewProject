from pydantic import BaseModel # type: ignore

class Book(BaseModel):
    """
    id, title, author, description, rating
    """
    id: int
    title: str
    author: str
    description: str
    rating: int
