from webbrowser import get
from xmlrpc.client import Boolean, boolean
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from pkg_resources import yield_lines
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db





router = APIRouter(
    prefix="",
    tags=['Filter']
)



@router.get("/filter/{category}",response_model=List[schemas.Post])
def filter_category(category : str,db: Session = Depends(get_db),limit:int = 10, skip: int = 0, search: Optional[str]=""):
    
    search = category
    posts = db.query(models.Post).filter(models.Post.category.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {category} was not found.")

    return posts


@router.get("/draft/{published}")
def filter_published(published : bool, db: Session = Depends(get_db), limit:int = 10, skip:int =0, search:Optional[bool]="",current_user: int= Depends(oauth2.get_current_user)):
    search = published
    # found_user = db.query(models.User).filter(models.User.id == id).first()
    print(search)
    found =  db.query(models.Post).filter((current_user.id == models.Post.owner_id))
    user_found = found.all()
    posts=  found.filter(models.Post.published == published).all()


    
    # final = dict(posts[1]).get('Post')
    # print(final)

    # for post in posts:
    #     hi =((post.Post))
    #     print(type(hi))

    # for i in posts:
    #     final =  (dict (posts[1]))
    #     print(final)
    #     hello  = (( (final.get('Post'))))
    #     bye = iter(hello)
    #     print(bye) 
            
            

    if (search == True):
        compare = 'Post'
    else:
        compare = 'Draft'

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{compare} was not found.")

    return posts



