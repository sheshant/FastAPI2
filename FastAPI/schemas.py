from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str]
    published_date: date


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    published_date: Optional[date]


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
