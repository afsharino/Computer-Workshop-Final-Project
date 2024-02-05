from pydantic import BaseModel

class Book(BaseModel):
    """
    Pydantic model representing a book.

    Attributes:
        title (str): The title of the book.
        rating (int): The rating of the book.
        author_id (int): The ID of the author associated with the book.

    Config:
        orm_mode (bool): Enables ORM mode for SQLAlchemy integration.
    :noindex:
    """

    title: str
    rating: int
    author_id: int

    class Config:
        """Pydantic configuration for the Book model."""
        orm_mode = True


class Author(BaseModel):
    """
    Pydantic model representing an author.

    Attributes:
        name (str): The name of the author.
        age (int): The age of the author.

    Config:
        orm_mode (bool): Enables ORM mode for SQLAlchemy integration.
    :noindex:
    """

    name: str
    age: int

    class Config:
        """Pydantic configuration for the Author model."""
        orm_mode = True
