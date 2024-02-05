# Import Libraries
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

Base = declarative_base()

class Book(Base):
    """
    SQLAlchemy model representing a book.

    Attributes:
        id (int): Primary key and unique identifier for the book.
        title (str): The title of the book.
        rating (int): The rating of the book.
        time_created (DateTime): The timestamp when the book record was created.
        time_updated (DateTime): The timestamp when the book record was last updated.
        author_id (int): Foreign key referencing the ID of the associated author.

    Relationships:
        author (relationship): Many-to-one relationship with the Author model.

    """

    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rating = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author")


class Author(Base):
    """
    SQLAlchemy model representing an author.

    Attributes:
        id (int): Primary key and unique identifier for the author.
        name (str): The name of the author.
        age (int): The age of the author.
        time_created (DateTime): The timestamp when the author record was created.
        time_updated (DateTime): The timestamp when the author record was last updated.

    """

    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
