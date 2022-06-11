
from cProfile import Profile
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi import UploadFile,File,Form

from app.models import User   

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id:int
    email: EmailStr
    firstName: str
    lastName: str
    profileImage: str

    class Config:
        orm_mode = True



class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id:int
    owner: UserOut
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr 
    password:str
    confirmPassword:str
    firstName:str
    lastName:str
    phoneNumber:int

    



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token = str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str] = None


class ForgotPasword(BaseModel):
    email:EmailStr
    class Config:
        orm_mode = True

class Password(BaseModel):
    email:Optional[EmailStr] = None
    password:str
    confirmPassword:Optional[str] = None




   