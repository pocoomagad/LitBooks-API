from service.books import Book_service
from service.users import AuthSerice
from repository.repository_db import AuthRepository, BookRepository, CartRepository
from auth.auth_config import authconfig
from service.cart import CartService
from fastapi import Depends
from typing import Annotated
from schemas.paginate import Paginate


def book_service():
    return Book_service(BookRepository)

def auth_service():
    return AuthSerice(AuthRepository, authconfig)

def user_cart_service():
    return CartService(CartRepository)

auth_ser = Annotated[AuthSerice, Depends(auth_service)]
cart_ser = Annotated[CartService, Depends(user_cart_service)]
paginate = Annotated[Paginate, Depends(Paginate)]
book_ser = Annotated[Book_service, Depends(book_service)]