from sqlalchemy import create_engine
from urllib.parse import quote
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from yaml import parse
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from .config import settings
SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" % quote(settings.database_password))

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine )

Base = declarative_base() 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='upama@123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connection to databse failed")
#         print("Error:", error)
#         time.sleep(2)
