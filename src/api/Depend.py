from service.books import Book_service
from service.users import AuthSerice
from repository.repository_db import AuthRepository, BookRepository, CartRepository
from auth.auth_config import authconfig
from service.cart import CartService


def book_service():
    return Book_service(BookRepository)

def auth_service():
    return AuthSerice(AuthRepository, authconfig)

def user_cart_service():
    return CartService(CartRepository)