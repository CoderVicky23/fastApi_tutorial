from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= {"detail": f"Blog with given Id {id} not found!"}
        )
    return blog

def delete(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    blog.delete(synchronize_session = False)
    db.commit()
    return { "response": "done" }

def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    # db.query(models.Blog).filter(models.Blog.id == id).update(
    #     { models.Blog.title : request.title, models.Blog.body : request.body },
    #     synchronize_session=False
    # )
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Blog with id {id}")
    blog.update(request.model_dump())
    db.commit()
    return { "response": "BLog Updated"}