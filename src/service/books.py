from repository.repository_db import Abstract_Repository
from schemas.newbook import BookSchema, BookSchemaPost

"""Слой сервисов"""

class Book_service:
    def __init__(self, books_repo: Abstract_Repository):
        self.books_repo: Abstract_Repository = books_repo()

    async def add_books(self, book: BookSchemaPost) -> dict:
        book_dict = book.model_dump()
        query = await self.books_repo.add_book(book_dict)
        return query
        

    async def return_books(self):
        query = await self.books_repo.return_book()
        result_dto = [BookSchema.model_validate(row, from_attributes=True) for row in query]
        return result_dto
    

    async def patch_books(self, book_id: int, book: BookSchemaPost):
        book_dict = book.model_dump()
        query = await self.books_repo.patch_book(book_id, book_dict)
        return query


    async def delete_books(self, book_id: int):
        query = await self.books_repo.delete_book(book_id)
        return query

