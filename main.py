import json

from fastapi import FastAPI, status, HTTPException

from pydantic import BaseModel
from typing import Optional

file_name = 'books.json'


class Book(BaseModel):
    id: int
    isbn: str
    title: str
    author: Optional[str] = None
    price: float = None


app = FastAPI()


@app.get('/books/')
async def get_books():
    with open(file_name) as f:
        books = json.load(f)

    return books


@app.get('/books/{id}')
async def get_book(id: int):
    with open(file_name) as f:
        books = json.load(f)

    for book in books:
        if book['id'] == id:
            return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


@app.post('/books/', status_code=status.HTTP_201_CREATED)
async def store_book(book: Book):
    with open(file_name) as f:
        books = json.load(f)

    if book.id in [book['id'] for book in books]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Resource already exists")

    books.append(book.dict())

    with open(file_name, 'w') as f:
        json.dump(books, f)

    return book


@app.put('/books/')
async def update_book(new: Book):
    with open(file_name) as f:
        books = json.load(f)

    for book in books:
        if book['id'] == new.id:
            book['isbn'] = new.isbn
            book['title'] = new.title
            book['author'] = new.author
            book['price'] = new.price
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    with open(file_name, 'w') as f:
        json.dump(books, f)

    return book


@app.delete('/books/{id}')
async def remove_book(id: int):
    with open(file_name) as f:
        books = json.load(f)

    for book in books:
        if book['id'] == id:
            books.remove(book)
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    with open(file_name, 'w') as f:
        json.dump(books, f)
