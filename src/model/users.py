from sqlalchemy import Index, text, VARCHAR, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from model.books import Base

class UserLoginModel(Base):
    __tablename__ = "users"

    user_name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(VARCHAR(64))
    
    __table_args__ = (
        Index("hash_password_idx", "password", postgresql_using='hash'),
    )