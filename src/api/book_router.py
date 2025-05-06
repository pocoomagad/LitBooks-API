from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from schemas.newbook import BookSchemaPost
from schemas.paginate import Paginate
from typing import Annotated
from service.books import Book_service
from api.Depend import book_service
from exceptions.handlers import *
from api.Depend import book_ser, paginate

book_rout = APIRouter(tags=["Books"])


"""Ручки книжек доступна только "авторам" """

@book_rout.get("/")
async def return_books(
    service: Annotated[Book_service, Depends(book_service)],
    paginate: paginate
    ):
    returning_res = await service.return_books(paginate)
    return returning_res
    
@book_rout.post("/litbooks")
async def add_book(
    book_id: BookSchemaPost, 
    service: book_ser
    ) -> JSONResponse:
    book_add = await service.add_books(book_id)
    return JSONResponse(status_code=200, content="Book add")


@book_rout.patch('/litbooks/{id}')
async def patch_book(
    id: int, 
    update_book: BookSchemaPost, 
    service: book_ser
    ) -> JSONResponse:
    book_patch = await service.patch_books(id, update_book)
    return JSONResponse(status_code=200, content=f"book has patched; id: {book_patch}")
    

@book_rout.delete('/litbooks/{id}')
async def delete_book(
    id: int,
    service: book_ser
    ) -> JSONResponse:
    book_deleted = await service.delete_books(book_id=id)
    return JSONResponse(status_code=200, content="Book has been deleted")



    