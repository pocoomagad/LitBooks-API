from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from api.Depend import auth_service, user_cart_service
from typing import Annotated
from service.users import AuthSerice
from service.cart import CartService
from authx import TokenPayload
from auth.auth_config import authconfig
from exceptions.handlers import *

user_rout = APIRouter(prefix="/profile")
auth_ser = Annotated[AuthSerice, Depends(auth_service)]
cart_ser = Annotated[CartService, Depends(user_cart_service)]



@user_rout.post("/create", tags=["Users"])
async def authorisation(
    auth_ser: auth_ser, 
    creds: UserLoginSchemaProfPost
                        ) -> JSONResponse:
    user_created = await auth_ser.create_users(creds)
    return JSONResponse("User created")

@user_rout.post("/login", response_class=RedirectResponse, status_code=302, tags=["Users"])
async def login(
    auth_ser: auth_ser,
    response: Response,
    input: UserLoginSchema
                ):
    user_login = await auth_ser.login(input)
    response.set_cookie(key="Authorization_token", value=user_login)
    return "http://127.0.0.1:8000/profile/me"
    

@user_rout.get("/me", tags=["Users"])
async def protected(
    auth_ser: auth_ser,
    token: TokenPayload = Depends(authconfig().security.access_token_required)
                    ) -> JSONResponse:
    user_protect = await auth_ser.get_profile(token)
    return user_protect


"""Круд корзины"""

@user_rout.post("/cart", tags=["Cart"])
async def add_into_cart_by_id(
    cart_ser: cart_ser,
    book_id: int,
    token: TokenPayload = Depends(authconfig().security.access_token_required)
    ) -> JSONResponse:
    user_cart = await cart_ser.add_to_cart(book_id, token)
    return JSONResponse(status_code=200, content="Add into cart")


@user_rout.delete("/cart", tags=["Cart"])
async def delete_from_cart_by_id(
    cart_ser: cart_ser,
    book_id: int,
    token: TokenPayload = Depends(authconfig().security.access_token_required)
    ) -> JSONResponse:
    delete_cart = await cart_ser.delete_from_cart(book_id, token)
    return JSONResponse(status_code=200, content="Delete from cart")
    