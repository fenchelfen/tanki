from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    cookie: str


class User(BaseModel):
    email: str
    cookie: str

    class Config:
        orm_mode = True
