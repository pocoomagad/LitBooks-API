from service.books import Book_service
from repository.repository_db import BookRepository
from service.users import AuthSerice
from repository.repository_db import AuthRepository
from auth.auth_config import authconfig


def book_service():
    return Book_service(BookRepository)

def auth_service():
    return AuthSerice(AuthRepository, authconfig)