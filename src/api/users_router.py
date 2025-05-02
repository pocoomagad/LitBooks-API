from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from api.Depend import auth_service, user_cart_service
from typing import Annotated
from service.users import AuthSerice
from service.cart import CartService
from authx import TokenPayload
from auth.auth_config import authconfig

user_rout = APIRouter(prefix="/profile", tags=["Users"])
auth_ser = Annotated[AuthSerice, Depends(auth_service)]
cart_ser = Annotated[CartService, Depends(user_cart_service)]



@user_rout.post("/create")
async def authorisation(
    auth_ser: auth_ser, 
    creds: UserLoginSchemaProfPost
                        ) -> JSONResponse:
    user_created = await auth_ser.create_users(creds)
    if user_created is not None:
        return user_created
    return JSONResponse("User created")

@user_rout.post("/login", response_class=RedirectResponse, status_code=302)
async def login(
    auth_ser: auth_ser,
    response: Response,
    input: UserLoginSchema
                ):
    user_login = await auth_ser.auths_in(input)
    if not user_login:
        raise HTTPException(status_code=401, detail={"Error": "Incorrect username or password"})
    response.set_cookie(key="Authorization_token", value=user_login)
    return "http://127.0.0.1:8000/profile/me"
    

@user_rout.get("/me")
async def protected(
    auth_ser: auth_ser,
    token: TokenPayload = Depends(authconfig().security.access_token_required)
                    ) -> JSONResponse:
    user_protect = await auth_ser.protecteds(token)
    if not user_protect:
        raise HTTPException(status_code=401, detail={"Error": str(user_protect)})
    return user_protect


"""Круд корзины"""

@user_rout.post("/cart")
async def get_cart_by_id(
    cart_ser: cart_ser,
    book_id: int,
    token: TokenPayload = Depends(authconfig().security.access_token_required)
    ) -> JSONResponse:
    try:
        user_cart = await cart_ser.add_to_cart(book_id, token)
        return user_cart
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"Error": str(e)})