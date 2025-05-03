# import pytest
# from contextlib import nullcontext as does_not_raise
# from src.service.books import Book_service, BookSchemaPost
# from src.repository.repository_db import BookRepository
# from pydantic import ValidationError
# from src.api.db_router import setup


# b = Book_service(BookRepository)

# info = {
#         "title": "string",
#         "author": "string",
#         "description": "stringstri",
#         "genres": "string",
#         "age_limit": "16+",
#         "price": 999999,
#         "isbn": "string"
#         }

# info1 = {
#         "title": "string",
#         "author": "string",
#         "description": "stringstri",
#         "genres": "string",
#         "age_limit": "asd",
#         "price": 999999909,
#         "isbn": "string"
#         }

# info2 = {
#         "title": "stringasdasdasdasdasdasdasfafsafafashasfa",
#         "author": "string",
#         "description": "stristri",
#         "genres": None,
#         "age_limit": "16+",
#         "price": 999999909,
#         "isbn": "string"
#         }

# @pytest.fixture(scope="module", autouse=True)
# def create_db():
#     setup()


# # @pytest.fixture
# # def books(self):
# #     books = [
# #         BookSchemaPost(**self.info),
# #         BookSchemaPost(**self.info1),
# #         BookSchemaPost(**self.info2)
# #     ]

# #     return books


# @pytest.mark.parametrize(
#         "book, excectation",
#         [
#             (BookSchemaPost(**info), does_not_raise()),
#             (BookSchemaPost(**info1), pytest.raises(ValidationError)),
#             (BookSchemaPost(**info2), pytest.raises(ValidationError)),
#         ]
#     )
# def test_books(book, excectation):
#     with excectation:
#         assert b.add_books(book) == None
    