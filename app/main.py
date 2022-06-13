from colorama import Cursor
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user, auth,filter
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# my_post = [{"title":"title of post1", "content":"content of post1", "id":1 },{"title":"favourite food", "content":"Ilike pizza" , "id":2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(filter.router)

@app.get("/")
def root():

    return {"message": "Welcome  api"}









