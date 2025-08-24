from pydantic import BaseModel, Field, ConfigDict

from .loans import PublicLoan


class BookBase(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str | None = None
    available_copies: int


class CreateBook(BookBase):
    pass


class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    published_year: int | None = None
    genre: str | None = None
    available_copies: int | None = None


class ShowBook(BookBase):
    id: int
    loans: list[PublicLoan] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
