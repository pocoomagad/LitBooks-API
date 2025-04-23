from fastapi import APIRouter, Depends, Response, HTTPException
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from web.Depend import auth_service
from typing import Annotated
from service.users import AuthSerice
from db.engines import conn, async_engine
from authx import RequestToken

user_rout = APIRouter(prefix="/profile", tags=["Users"])


@user_rout.post("/create")
async def authorisation(
    auth_ser: Annotated[AuthSerice, Depends(auth_service)], 
    creds: UserLoginSchemaProfPost
                        ):
    user_created = await auth_ser.create_users(creds)
    if not user_created:
        return user_created
    return {"User": "created"}

@user_rout.post("/login")
async def login(
    input: UserLoginSchema, 
    auth_ser: Annotated[AuthSerice, Depends(auth_service)]
                ):
    user_login = await auth_ser.auths_in(input)
    if not user_login:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return user_login


@user_rout.get("/author")
async def protected(
    token: RequestToken,
    auth_ser: Annotated[AuthSerice, Depends(auth_service)]
                    ):
    user_protect = await auth_ser.protecteds(token)
    if not user_protect:
        raise HTTPException(status_code=401, detail={"error": "Access denied"})
    return user_protect