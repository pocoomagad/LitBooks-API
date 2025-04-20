from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Index, text, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
import datetime
from schemas.newbook import BookSchema


"""Модель книги"""


class Base(DeclarativeBase):
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<({self.__class__.__name__})>"
    

timezone = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    author: Mapped[str]
    description: Mapped[str]
    genres: Mapped[str | None]
    public_at: Mapped[timezone]
    age_limit: Mapped[str] = mapped_column(VARCHAR())
    price: Mapped[int]
    isbn: Mapped[str] = mapped_column(unique=True)
    
    __table_args__ = (
        Index("titles_index", "title"),
    )


    