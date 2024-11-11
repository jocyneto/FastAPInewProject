from fastapi import APIRouter # type: ignore
from models.book import Book

router = APIRouter()

BOOKS = [
    Book(id=1, title='Computer Science Pro', author='codingwithroby', description='A very nice book!', rating=5),
    Book(id=2, title='Be Fast with FastAPI', author='codingwithroby', description='A great book!', rating=5),
    Book(id=3, title='Master Endpoints', author='codingwithroby', description='A awesome book!', rating=5),
    Book(id=4, title='HP1', author='Author 1', description='Book Description', rating=2),
    Book(id=5, title='HP2', author='Author 2', description='Book Description', rating=3),
    Book(id=6, title='HP3', author='Author 3', description='Book Description', rating=1)
]

@router.get("/books")
async def get_all():
    return BOOKS
