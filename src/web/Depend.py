from service.books import Book_service
from repository.repository_db import BookRepository


def book_service():
    return Book_service(BookRepository)