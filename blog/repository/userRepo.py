from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, hashing

def get_all(db: Session):
    users = db.query(models.Users).all()
    return users

def create(request: schemas.User, db: Session):
    hashedPassword = hashing.Hash.bcrypt(request.password)
    new_user = models.Users(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user

def show(id, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user