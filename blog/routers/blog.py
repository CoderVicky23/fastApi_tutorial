from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, oauth2
from ..database import get_db
from typing import List

from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

@router.get("/", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, db)

@router.delete("/{id}")
def destroy(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id, db)

@router.put("/{id}")
def update(id, request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)