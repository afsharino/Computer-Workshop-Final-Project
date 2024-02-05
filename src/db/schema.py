from pydantic import BaseModel

class Book(BaseModel):
    """Book schema."""
    title: str
    rating: int
    author_id: int

    class Config:
        orm_mode = True

class Author(BaseModel):
    """Author schema."""
    name: str
    age: int

    class Config:
        orm_mode = True
