from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from typing import List

from ..repository import userRepo

router = APIRouter(
    prefix="/user",
    tags = ['Users']
)

@router.get("/", response_model=List[schemas.ShowUser])
def showUser(db: Session = Depends(get_db)):
    return userRepo.get_all(db)

@router.post("/")
def user(request: schemas.User, db: Session = Depends(get_db)):
    return userRepo.create(request, db)

@router.get("/{id}", response_model = schemas.ShowUser)
def showUser(id, db: Session = Depends(get_db)):
    return userRepo.show(id, db)