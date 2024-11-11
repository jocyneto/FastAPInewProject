from datetime import datetime
from fastapi import APIRouter, Path, Query, HTTPException
from models.book import Book
from starlette import status

router = APIRouter()

BOOKS = [
    Book(id=1, title='Computer Science Pro', author='codingwithroby', description='A very nice book!', rating=5, published_date=2023),
    Book(id=2, title='Be Fast with FastAPI', author='codingwithroby', description='A great book!', rating=5, published_date=2023),
    Book(id=3, title='Master Endpoints', author='codingwithroby', description='A awesome book!', rating=5, published_date=2024),
    Book(id=4, title='HP1', author='Author 1', description='Book Description', rating=2, published_date=2003),
    Book(id=5, title='HP2', author='Author 2', description='Book Description', rating=3, published_date=2002),
    Book(id=6, title='HP3', author='Author 3', description='Book Description', rating=1, published_date=2013)
]

@router.get("/books", status_code=status.HTTP_200_OK)
async def get_all():
    return BOOKS

@router.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt = 0)):
    for b in BOOKS:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Item not found!")

@router.get("/books/get_by_rating/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(ge=1, le=5)):
    books_return = []
    for b in BOOKS:
        if b.rating == book_rating:
            books_return.append(b)
    return books_return

@router.get("/books/get_by_published_date/", status_code=status.HTTP_200_OK)
async def get_by_published_date(date_year: int = Query(ge=1900, le=datetime.now().year)):
    books_return = []
    for b in BOOKS:
        if b.published_date == date_year:
            books_return.append(b)
    return books_return

@router.post("/books/add", status_code=status.HTTP_201_CREATED)
async def add_book(new_book: Book):
    BOOKS.append(find_book_id(new_book))


@router.put("/books/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(udpate_book: Book):
    book_change = False
    book_found = await get_book_by_id(udpate_book.id)
    if book_found is not None:
        for i in range(len(BOOKS)):
            if BOOKS[i].id ==  book_found.id:
                BOOKS[i] = udpate_book
                book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found!") 

@router.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            return
    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found!")


#region Util Funcs
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
#endregion
