from pydantic import BaseModel
from typing import List
from schemas.newbook import BookSchema

class CartSchema(BaseModel):
    book: BookSchema