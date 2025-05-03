from pydantic import BaseModel, Field

class Paginate(BaseModel):
    offset: int 
    limit: int