from os import environ

from fastapi import FastAPI, status, Body, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List
from models import Book

from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(environ.get('MONGO_URL'))
    app.db = app.mongodb_client[environ.get('MONGO_DB_NAME')]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get('/', tags=['Root'])
def index():
    return JSONResponse({'message': 'Welcome to our Bookstore!'})


@app.get('/books/', tags=['Books'], response_description="List all books", response_model=List[Book])
async def get_books():
    books = await app.db["books"].find().to_list(100)
    return books


@app.get('/books/{isbn}', tags=['Books'], response_description='Get a single book', response_model=Book)
async def get_book(isbn: str):
    if (book := await app.db["books"].find_one({"isbn": isbn})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ISBN '{isbn}' was not found")


@app.post('/books/', tags=['Books'], response_description='Add new student', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book = Body(...)):
    isbn = book.isbn
    book = jsonable_encoder(book)

    if (existing := await app.db["books"].find_one({"isbn": isbn})) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Book with ISBN '{isbn}' already exists")

    new = await app.db["books"].insert_one(book)
    created = await app.db["books"].find_one({"_id": new.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created)


@app.put("/books/", tags=['Books'], response_description="Update a book", response_model=Book)
async def update_book(book: Book = Body(...)):
    isbn = book.isbn
    book = {k: v for k, v in book.dict().items() if k != 'id' and v is not None}

    if len(book) >= 1:
        result = await app.db["books"].update_one({"isbn": isbn}, {"$set": book})

        if result.modified_count == 1:
            if (updated := await app.db["books"].find_one({"isbn": isbn})) is not None:
                return updated

    if (existing := await app.db["books"].find_one({"isbn": isbn})) is not None:
        return existing

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ISBN '{isbn}' was not found")


@app.delete("/books/{isbn}", tags=['Books'], response_description="Delete a book")
async def delete_book(isbn: str):
    result = await app.db["books"].delete_one({"isbn": isbn})

    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ISBN '{isbn}' was not found")
