import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from fastapi.testclient import TestClient
from src.api.main import app
from src.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Author as ModelAuthor
import pytest

# Use database for testing
SQLALCHEMY_DATABASE_URL = "postgresql://afsharino:12345678@db:5432/book_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "HI Welcome to RestAPI"}


def test_add_author(db):
    response = client.post(
        "/add-author/",
        json={"name": "Test Author", "age": 30},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Author"
    assert response.json()["age"] == 30

    # Check if the author is added to the database
    author = db.query(ModelAuthor).filter_by(name="Test Author").first()
    print("Author in the database:", author)  # Add this line for debugging
    assert author is not None

def test_add_book(db):
    # Add a test author
    response_author = client.post(
        "/add-author/",
        json={"name": "Test Author", "age": 30},
    )
    assert response_author.status_code == 200
    author_id = response_author.json().get("id")

    # Add a book with invalid data (for testing validation error)
    response_book = client.post(
        "/add-book/",
        json={"title": "Test Book", "rating": "invalid_rating", "author_id": author_id},
    )
    assert response_book.status_code == 422  # Expecting a validation error
