
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from sqlalchemy import null

from app.models import User   

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True
    category: str

class PostCreate(BaseModel):
    title: Optional [str] 
    content: Optional [str]
    published: bool = True
    category: Optional [str]

# register garne bela profileImage rakhna mildaina
# tara malai profile Image getAllPosts garne bela chainxa
# so conflicting bhayo...
class UserOut(BaseModel):
    id:int
    email: EmailStr
    firstName: str
    lastName: str 

    class Config:
        orm_mode = True

class GetUser(UserOut):
    profileImage : str

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id:int
    owner: UserOut
    class Config:
        orm_mode = True

class PostUpdate(PostCreate):
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




   