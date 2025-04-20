from fastapi import FastAPI
from web.book_router import db_rout

app = FastAPI()
app.include_router(db_rout)