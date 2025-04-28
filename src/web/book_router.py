from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from schemas.newbook import BookSchemaPost
from typing import Annotated
from service.books import Book_service
from web.Depend import book_service

book_rout = APIRouter(tags=["Books"])

"""Ручки книжек доступна только "авторам" """

@book_rout.get("/")
async def return_books(
    service: Annotated[Book_service, Depends(book_service)]
    ) -> JSONResponse:
    returning_res = await service.return_books()
    return JSONResponse(status_code=200, content=returning_res)
    
@book_rout.post("/litbooks")
async def add_book(
    book_id: BookSchemaPost, 
    service: Annotated[Book_service, Depends(book_service)]
    ) -> JSONResponse:
    book_add = await service.add_books(book_id)
    if book_add is None:
        return JSONResponse(status_code=200, content="Book add")
    return HTTPException(detail=book_add, status_code=400)


@book_rout.patch('/litbooks/{id}')
async def patch_book(
    id: int, 
    update_book: BookSchemaPost, 
    service: Annotated[Book_service, Depends(book_service)]
    ) -> JSONResponse:
    book_patch = await service.patch_books(id, update_book)
    if not book_patch:
        raise HTTPException(status_code=404, detail="Book not found")
    return JSONResponse(status_code=200, content=f"book has patched; id: {book_patch}")
    

@book_rout.delete('/litbooks/{id}')
async def delete_book(
    id: int,
    service: Annotated[Book_service, Depends(book_service)],
    ) -> JSONResponse:
    book_deleted = await service.delete_books(book_id=id)
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return JSONResponse(status_code=200, content="Book has been deleted")



    