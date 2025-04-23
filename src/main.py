from fastapi import FastAPI
from web.book_router import book_rout
from web.users_router import user_rout
from web.db_router import db_rout
from fastapi import middleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    )
app.include_router(book_rout)
app.include_router(user_rout)
app.include_router(db_rout)