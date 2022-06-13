from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db





router = APIRouter(
    prefix="/filter",
    tags=['Filter']
)
@router.get("/{category}",response_model=List[schemas.Post])
def filter_category(category : str,db: Session = Depends(get_db),limit:int = 10, skip: int = 0, search: Optional[str]=""):
    
    search = category
    posts = db.query(models.Post).filter(models.Post.category.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {category} was not found.")

    return posts
