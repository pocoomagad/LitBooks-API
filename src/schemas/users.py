from pydantic import BaseModel, Field, field_validator, EmailStr, computed_field

class UserLoginSchemaGet(BaseModel):
    user_name: str
    password: str
    email: EmailStr

    @computed_field
    def protected_password(self) -> str:
        return f"{len(self.password) * "*"}"


class UserLoginSchemaProfPost(BaseModel):
    user_name: str  = Field(min_length=5, max_length=32)
    password: str = Field(min_length=8)
    email: EmailStr


class UserLoginSchema(BaseModel):
    user_name: str 
    password: str 
