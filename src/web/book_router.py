from fastapi import APIRouter, HTTPException, Depends
from schemas.newbook import BookSchemaPost
from typing import Annotated
from service.books import Book_service
from web.Depend import book_service
from authx import TokenPayload
from auth.auth_config import authconfig
from authx.exceptions import MissingTokenError


book_rout = APIRouter(prefix="/litbooks", tags=["Books"])


"""Ручки книжек доступна только "авторам" """

@book_rout.get("")
async def return_books(
    service: Annotated[Book_service, Depends(book_service)]
    ):
    returning_res = await service.return_books()
    return returning_res


@book_rout.post("")
async def add_book(
    book_id: BookSchemaPost, 
    service: Annotated[Book_service, Depends(book_service)],
    payload: TokenPayload = Depends(authconfig().security.access_token_required)
    ):
    
    check = getattr(payload, "author")
    if not check:
        raise HTTPException(status_code=401, detail="You are not an author")
    book_add = await service.add_books(book_id)
    if book_add is None:
        return {"Book": "add"}
    return HTTPException(detail=book_add, status_code=400)


@book_rout.patch('/{id}')
async def patch_book(
    id: int, 
    update_book: BookSchemaPost, 
    service: Annotated[Book_service, Depends(book_service)]):
    book_patch = await service.patch_books(id, update_book)
    if not book_patch:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book has patched; id:": book_patch}
    

@book_rout.delete('/{id}')
async def delete_book(
    id: int,
    service: Annotated[Book_service, Depends(book_service)]
    ):
    book_deleted = await service.delete_books(book_id=id)
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"Book": "deleted"}



    