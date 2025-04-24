from fastapi import APIRouter, Depends, Response, HTTPException
from schemas.users import UserLoginSchemaProfPost, UserLoginSchema
from web.Depend import auth_service
from typing import Annotated
from service.users import AuthSerice
from db.engines import conn, async_engine
from authx import RequestToken
from auth.auth_config import authconfig

user_rout = APIRouter(prefix="/profile", tags=["Users"])


@user_rout.post("/create")
async def authorisation(
    auth_ser: Annotated[AuthSerice, Depends(auth_service)], 
    creds: UserLoginSchemaProfPost
                        ):
    user_created = await auth_ser.create_users(creds)
    if user_created is not None:
        return user_created
    return {"User": "created"}

@user_rout.post("/login")
async def login(
    input: UserLoginSchema, 
    auth_ser: Annotated[AuthSerice, Depends(auth_service)],
    responce: Response
                ):
    user_login = await auth_ser.auths_in(input)
    if not user_login:
        raise HTTPException(status_code=401, detail={"Error": "Incorrect username or password"})
    responce.set_cookie(authconfig.responce, user_login)
    return {"access_token": user_login}
    

@user_rout.get("", dependencies=[Depends(authconfig.security.get_token_from_request)])
async def protected(
    auth_ser: Annotated[AuthSerice, Depends(auth_service)],
    token: RequestToken = Depends(),
                    ):
    user_protect = await auth_ser.protecteds(token)
    if not user_protect:
        raise HTTPException(status_code=401, detail={"Error": str(user_protect)})
    return user_protect 