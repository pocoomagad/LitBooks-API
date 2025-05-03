from __future__ import annotations
from sqlalchemy import Index, text, VARCHAR, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from model.basic import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""Модель корзины"""

class CartModel(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), unique=True)

    book: Mapped[list["BookModel"]] = relationship(
        back_populates="carts",
        lazy='subquery'
        )
    user: Mapped["UserLoginModel"] = relationship(
        back_populates="cart"
        )