
from random import randrange
from re import U
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostLike])

# @router.get("/")
async def get_Post(db: Session = Depends(get_db), limit:int = 10, skip: int = 0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.published == True and models.Post.title.contains(search)).limit(limit).offset(skip)
    # post = posts.all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.published == True , models.Post.title.contains(search)).limit(limit).offset(skip).all()

    a=[]
    u=[]
    for i in range(len(results)):
        post = results[i]._asdict()
        hello = post['Post'].__dict__
        hello['likes'] = post['likes']
        a.append(hello)

 

    for i in range(len(results)):
        final = db.query(models.User).filter(models.User.id == a[i]['owner_id']).first()
        y =(final.__dict__)
        b =a[i]
        b['profileImage'] = y['profileImage']
        u.append(b)


    return u



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # # conn.commit()
    # print(current_user.id)
    # print(current_user.email)
    new_post=models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}" ,response_model= schemas.PostLike)
def get_post(id: int, db: Session = Depends(get_db)):


    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with {id} was not found." }

    post = results._asdict()
    hello = post['Post'].__dict__
    hello['likes'] = post['likes']
    final = db.query(models.User).filter(models.User.id == hello['owner_id']).first()
    y =(final.__dict__)
    hello['profileImage'] = y['profileImage']

    return hello




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)),)
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with {id} doesnot exist.")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schemas.PostUpdate)
def update_post(id: int,updated_post: schemas.PostCreate,  db: Session = Depends(get_db),current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)),)
    # updated_post = cursor.fetchone() 
    # conn.commit()
    print(updated_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with {id} doesnot exist.")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    if(updated_post.title == None):
        updated_post.title = post.title
    if(updated_post.category == None):
        updated_post.category = post.category
    if(updated_post.content == None):
        updated_post.content = post.content

    print(updated_post)


    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()



   
