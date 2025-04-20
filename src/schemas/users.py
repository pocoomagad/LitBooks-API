from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr, computed_field

class UserLoginSchema(BaseModel):
    user_name: str
    password: str
    email: EmailStr

    @computed_field
    def protected_password(self) -> str:
        return f"{len(self.password) * "*"}"


class UserLoginSchemaProfPost(BaseModel):
    user_name: str | None = Field(min_length=1, max_length=32)
    password: str = Field(min_length=8)
    email: EmailStr

    @field_validator("user_name")
    def user_check_(cls, value):
        if value is None:
            cls.user_name = cls.email
