"""
Module containing test functions for the FastAPI application.

This module includes test functions for the main FastAPI application.
It utilizes the TestClient from FastAPI to perform HTTP requests and
validates the responses. It also sets up a testing database using
SQLAlchemy and pytest fixtures.

Tested Endpoints:
- GET /: Tests the root endpoint of the FastAPI application.
- POST /add-author/: Tests the endpoint for adding an author.
- POST /add-book/: Tests the endpoint for adding a book.

Note: This module assumes a PostgreSQL database at the specified URL
for testing purposes.

Author: [Your Name]

"""

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
    """
    Pytest fixture for creating and closing a testing database session.

    This fixture sets up a testing database session using SQLAlchemy
    and yields the database session to be used in test functions.
    The session is automatically closed after the tests.

    Returns:
        SQLAlchemy database session: A testing database session.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_read_main():
    """
    Test function for the root endpoint.

    This function sends a GET request to the root endpoint of the FastAPI
    application and asserts the expected HTTP status code and response JSON.

    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "HI Welcome to RestAPI"}


def test_add_author(db):
    """
    Test function for the endpoint to add an author.

    This function sends a POST request to the /add-author/ endpoint with
    sample data and asserts the expected HTTP status code and response JSON.
    It also checks if the added author is present in the testing database.

    Args:
        db: Pytest fixture providing a testing database session.

    """
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
    """
    Test function for the endpoint to add a book.

    This function sends a POST request to the /add-book/ endpoint with
    sample data and asserts the expected HTTP status code.
    It adds a test author first and then attempts to add a book with
    invalid data to test the validation error.

    Args:
        db: Pytest fixture providing a testing database session.

    """
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
