from fastapi import Body, APIRouter # type: ignore

router = APIRouter()

BOOKS = [
    {"id": 1,"title": "Title Two", "author": "Author Two", "category": "science"},
    {"id": 2,"title": "Title One", "author": "Author One", "category": "science"},
    {"id": 3,"title": "Title Three", "author": "Author Three", "category": "history"},
    {"id": 4,"title": "Title Four", "author": "Author Four", "category": "math"},
    {"id": 5,"title": "Title Five", "author": "Author Five", "category": "math"},
    {"id": 6,"title": "Title Six", "author": "Author Two", "category": "math"}
]

@router.get("/")
async def first_api():
    return {"text":"Hello world!"}

@router.get("/books")
async def get_all_books():
    return BOOKS

@router.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.get("id") == book_id:
            return book

@router.get("/books/")
async def get_book_by_author(author: str):
    return_books = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            return_books.append(book)
    
    return return_books

@router.get("/books/{book_category}/")
async def get_book_author_by_category(book_category:str, author:str):
    return_books = []
    for book in BOOKS:
        if author.casefold() == book.get("author").casefold() \
            and book_category.casefold() == book.get("category").casefold():
            return_books.append(book)
    
    return return_books

@router.post("/books/create_book/")
async def create_new_book(new_book=Body("default")):
    BOOKS.append(new_book)

@router.put("/books/update_book/{book_id}")
async def update_book_by_id(book_id: int, update_book=Body("default")):
    new_book_for_update = await read_book(book_id)
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == new_book_for_update.get("id"):
            BOOKS[i] = update_book

@router.delete("/books/delete_book/{book_id}")
async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == book_id:
            BOOKS.pop(i)
