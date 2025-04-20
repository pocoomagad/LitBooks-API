from fastapi import APIRouter, HTTPException, Depends
from schemas.newbook import BookSchemaPost
from typing import Annotated
from service.books import Book_service
from web.Depend import book_service
from model.books import Base


db_rout = APIRouter(prefix="/litbooks", tags=["Books"])

"""Ручки книжек доступна только "авторам" """

@db_rout.post("")
async def add_book(
    book_id: BookSchemaPost, 
    service: Annotated[Book_service, Depends(book_service)]):
    book_add = await service.add_books(book_id)
    if book_add is None:
        return {"Book": "add"}
    return HTTPException(detail=book_add, status_code=400, headers="")


@db_rout.patch('/{id}')
async def patch_book(
    id: int, 
    update_book: BookSchemaPost, 
    service: Annotated[Book_service, Depends(book_service)]):
    book_patch = await service.patch_books(id, update_book)
    return {"book has patched; id:": book_patch}

@db_rout.get("")
async def return_books(service: Annotated[Book_service, Depends(book_service)]):
    returning_res = await service.return_books()
    return returning_res
    

@db_rout.delete('/{id}')
async def delete_book(
    id: int,
    service: Annotated[Book_service, Depends(book_service)]
                      ):
    book_deleted = await service.delete_books(book_id=id)
    return {"Book": "deleted"}



    