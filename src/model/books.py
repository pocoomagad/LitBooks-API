from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Index, text, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
import datetime
from model.basic import Base

"""Модель книги"""

"""Если вы используете postgresql"""
# server_default=text(
# "TIMEZONE('utc', now())",
"""Если вы используете sqlite"""

timezone = Annotated[datetime.datetime, mapped_column(
    # server_default=text(
    # "TIMEZONE('utc', now())"))]
    default=datetime.datetime.now())]


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

    from model.cart import CartModel

    carts: Mapped[list["CartModel"]] = relationship(
        back_populates="book"
        )
    
    __table_args__ = (
        Index("titles_index", "title"),
    )


    