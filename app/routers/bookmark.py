from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import false, func
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from ..database import get_db
router = APIRouter(
    prefix="/bookmark",
    tags=['Bookmark']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def bookmark(bookmark: schemas.Bookmark, db: Session = Depends(database.get_db), current_user: int= Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == bookmark.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {bookmark.post_id} does not exist.")

    bookmark_query = db.query(models.Bookmark).filter(models.Bookmark.post_id == bookmark.post_id, models.Bookmark.user_id == current_user.id)
    found_bookmark = bookmark_query.first()

    if(bookmark.dir == 1):
        if found_bookmark:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {bookmark.post_id}")

        new_bookmark = models.Bookmark(post_id = bookmark.post_id, user_id = current_user.id)
        db.add(new_bookmark)
        db.commit()
        return{"message":"Successfully added bookmark"}
    else:
        if not found_bookmark:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark doesn't exist")
        
        
        bookmark_query.delete(synchronize_session=False)
        db.commit()    


        return{"message":"Succesfully deleted bookmark"}


@router.get('/received', response_model=List[schemas.BookmarkUser])
def userBookmark(db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ,limit:int=10, skip: int =0, search: Optional[str]="" ):

    results = db.query(models.Post, func.count(models.Bookmark.post_id).label("Bookmarked")).join(models.Bookmark, models.Bookmark.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.published == True,models.Bookmark.user_id == current_user.id , models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    a=[]

    for i in range(len(results)):
        post = results[i]._asdict()
        newPost = post['Post'].__dict__
        newPost['bookmarked'] = post['Bookmarked']
        a.append(newPost)

    return a

