from fastapi import FastAPI, Request, HTTPException, Depends
from api.book_router import book_rout
from api.users_router import user_rout
from api.db_router import db_rout
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from authx import TokenPayload, RequestToken
from auth.auth_config import authconfig
from authx.exceptions import MissingTokenError
from exceptions.handlers import *   

app = FastAPI(description="This is openapi project by pocoomagad")

@app.exception_handler(NotFoundException)
async def not_found_exc(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"Error": f"Book not found"}
        )


@app.exception_handler(IsbnUniqueException)
async def isbn_unique_exc(request: Request, exc: IsbnUniqueException):
    return JSONResponse(
        status_code=400,
        content={"Error": "isbn must be unique"}
        )


@app.exception_handler(PasswordException)
async def pass_exc(request: Request, exc: PasswordException):
    return JSONResponse(
        status_code=400,
        content={"Error": "Incorrect username or password"}
        )


@app.exception_handler(CartException)
async def cart_exc(request: Request, exc: CartException):
    return JSONResponse(
        status_code=208,
        content={"Error": "Book already in cart"}
    )


@app.exception_handler(AlreadyInUse)
async def pass_exc(request: Request, exc: AlreadyInUse):
    return JSONResponse(
        status_code=208,
        content={"Error": "Password or username already use"}
    )


class AuthorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.access_token = authconfig().security.access_token_required

    async def dispatch(self, request: Request, call_next):
        if "litbooks" in request.url.path:
            try:
                token_payload: TokenPayload = await self.access_token(request)

                check = getattr(token_payload, "author")
                if not check:
                    return JSONResponse(
                        status_code=403, content="You are not an author"
                        )
            except MissingTokenError:
                return JSONResponse(
                    status_code=401, content="Please log in"
                    )
            

            response = await call_next(request)
            response.headers["X-Page-Title"] = "LitBooks Page"
            return response
        return await call_next(request)
    

class UserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth = authconfig().security.access_token_required


    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/profile/me" or request.url.path == "/profile/cart":
            try:
                token: TokenPayload = await self.auth(request)

                if not self.auth:
                    return JSONResponse(
                        status_code=401, content="Please log in"
                    )
            except MissingTokenError:
                return JSONResponse(
                        status_code=401, content="Please log in"
                        )
            

            response = await call_next(request)
            response.headers["X-Page-Title"] = "User Page"
            return response 
        return await call_next(request)


app.include_router(book_rout)
app.include_router(user_rout)
app.include_router(db_rout)
app.add_middleware(AuthorMiddleware)
app.add_middleware(UserMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )