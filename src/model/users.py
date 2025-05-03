from __future__ import annotations
from sqlalchemy import Index, text, VARCHAR, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from model.basic import Base

"""Модель юзера"""

class UserLoginModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(64))
    author: Mapped[bool] 

    from model.cart import CartModel

    cart: Mapped[list["CartModel"]] = relationship(
        back_populates="user",
        passive_deletes=True
        )
    
    __table_args__ = (
        Index("hash_password_idx", "password", postgresql_using='hash'),
    )