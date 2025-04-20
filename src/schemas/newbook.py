from pydantic import BaseModel, Field, field_validator, ConfigDict
import re
import datetime

class BookSchema(BaseModel):
    id: int

    title: str 
    author: str 
    description: str 
    genres: str | None
    age_limit: str
    public_at: datetime.datetime
    price: int 
    isbn: str
    
class BookSchemaPost(BaseModel):
    title: str = Field(max_length=30, min_length=1)
    author: str = Field(max_length=50, min_length=1)
    description: str = Field(max_lenght=180, min_length=10)
    genres: str | None 
    age_limit: str
    price: int = Field(lt=1000000, ge=0)
    isbn: str = Field(max_length=32)

    @field_validator('age_limit')
    def check_right_data(cls, value):
        pattern = r"^(18|16|12|6|0)\+$"

        if re.match(pattern, value):
            return value
        raise ValueError('Неправильно заполненное поле "age_limit"')