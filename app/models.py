
from sqlalchemy import  Column, ForeignKey, Integer,String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import DateTime
from .database import Base
import datetime


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False )
    title = Column(String, nullable= False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default='TRUE', nullable = False)
    category = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False,server_default=text('now()') )  
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False )
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable = False)
    confirmPassword= Column(String, nullable = False)
    firstName= Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    phoneNumber = Column(String,unique=True, nullable=False)
    profileImage = Column(String , nullable= True)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False,server_default=text('now()') )  

class Code(Base):
    __tablename__ = "codes"
    id = Column(Integer, primary_key=True, nullable = False)
    reset_code = Column(String)
    expires_in = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    owner = relationship("User")
