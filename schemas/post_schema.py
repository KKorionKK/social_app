from pydantic import BaseModel
from datetime import datetime

class PostCreateSchema(BaseModel):
    header: str
    description: str
    created: datetime

    class Config:
        orm_mode = True


class PostUpdateSchema(BaseModel):
    id: int
    header: str
    description: str

    class Config:
        orm_mode = True


class PostSchema(PostCreateSchema):
    id: int
    user_id: int

    class Config:
        orm_mode = True