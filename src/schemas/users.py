from schemas.cart import CartSchema
from pydantic import BaseModel, Field, field_validator, EmailStr, computed_field, ConfigDict
from typing import Optional, List

class UserLoginSchemaGet(BaseModel):
    user_name: str
    password: str 
    email: EmailStr
    author: bool
    cart: List[CartSchema] | None


    @field_validator('password', mode='after')
    @classmethod
    def get_validate(cls, v):
        return "******"


class UserLoginSchemaProfPost(BaseModel):
    user_name: str = Field(min_length=5, max_length=32)
    password: str = Field(min_length=8)
    email: Optional[EmailStr] = None
    author: bool


class UserLoginSchema(BaseModel):
    user_name: str = Field(min_length=5, max_length=32)
    password: str = Field(min_length=8)
