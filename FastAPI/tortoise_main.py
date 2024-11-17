from fastapi import FastAPI, HTTPException
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from FastAPI.models import Book
from FastAPI.schemas import BookCreate, BookUpdate, BookResponse

app = FastAPI()


# CRUD Operations

@app.post("/books/", response_model=BookResponse)
async def create_book(book: BookCreate):
    new_book = await Book.create(**book.model_dump())
    return BookResponse.from_orm(new_book)


@app.get("/books/{book_id}/", response_model=BookResponse)
async def get_book(book_id: int):
    try:
        book = await Book.get(id=book_id)
        return await BookResponse.from_tortoise_orm(book)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", response_model=list[BookResponse])
async def list_books():
    books = await Book.all()
    return [BookResponse.from_orm(book) for book in books]


@app.put("/books/{book_id}/", response_model=BookResponse)
async def update_book(book_id: int, book_update: BookUpdate):
    try:
        book = await Book.get(id=book_id)
        for key, value in book_update.dict(exclude_unset=True).items():
            setattr(book, key, value)
        await book.save()
        return await BookResponse.from_tortoise_orm(book)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}/", status_code=204)
async def delete_book(book_id: int):
    try:
        book = await Book.get(id=book_id)
        await book.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")



Tortoise.init_models(["FastAPI.models"], "models")


# Register Tortoise ORM
register_tortoise(
    app,
    db_url="postgres://postgres:rootuser@localhost:5432/elastic",
    modules={"models": ["FastAPI.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
