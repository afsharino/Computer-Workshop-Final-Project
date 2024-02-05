# Import Libraries
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from src.db.models import Author
from src.db.models import Author as ModelAuthor
from src.db.models import Book
from src.db.models import Book as ModelBook
from src.db.schema import Author as SchemaAuthor
from src.db.schema import Book as SchemaBook

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get('/')
async def root():
    """
    Root endpoint.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {'message' : 'HI Welcome to RestAPI'}

@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    """
    Endpoint to add a book.

    Args:
        book (SchemaBook): The book information.

    Returns:
        ModelBook: The added book.
    """
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.post("/add-author/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    """
    Endpoint to add an author.

    Args:
        author (SchemaAuthor): The author information.

    Returns:
        ModelAuthor: The added author.
    """
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get("/books/")
def get_books():
    """
    Endpoint to get all books.

    Returns:
        list: A list of books.
    """
    books = db.session.query(Book).all()
    return books
