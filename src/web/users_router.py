from fastapi import APIRouter, HTTPException, Depends, Response
from authx import AuthX, AuthXConfig
from schemas.users import UserLoginSchemaProfPost

user_rout = APIRouter("/profile")

@user_rout.post("/login")
async def login(creds: UserLoginSchemaProfPost):
    if login:
        pass
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@user_rout.get("/protected")
async def protected():
    pass