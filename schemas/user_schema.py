from pydantic import BaseModel
from datetime import datetime

class UserCreateSchema(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    created: datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: str
    surname: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserSchema(UserCreateSchema):
    id: int