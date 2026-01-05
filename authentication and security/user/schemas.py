from pydantic import BaseModel
from typing import List


class User(BaseModel):
    name: str
    age: int
    phone: int
    
    class Config:
        orm_mode = True

class LoginDetails(BaseModel):
    name: str
    email: str
    password: str

class ShowLoginDetails(BaseModel):
    name: str
    email: str
    user: List[User]

    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    
    name: str
    age: int
    phone: int
    login_details : ShowLoginDetails
    
    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None