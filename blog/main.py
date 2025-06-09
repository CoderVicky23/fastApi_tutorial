# 2:38:00

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, hashing
from .database import engine, SessionLocal
from typing import List





app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= {"detail": f"Blog with given Id {id} not found!"}
        )
    return blog

@app.delete("/blog/{id}")
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    blog.delete(synchronize_session = False)
    db.commit()
    return { "response": "done" }

@app.put("/blog/{id}")
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
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





@app.post("/user", tags=["user"])
def user(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = hashing.Hash.bcrypt(request.password)
    new_user = models.Users(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user", response_model=List[schemas.ShowUser], tags=['user'])
def showUser(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

@app.get("/user/{id}", response_model = schemas.ShowUser, tags=['user'])
def showUser(id, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user










# if (__name__ == "__main__"):
#     uvicorn.run(app, host="127.0.0.1", port=9000)