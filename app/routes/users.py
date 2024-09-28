from fastapi import APIRouter, Response, status, Depends, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..utils import hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.Create_user, db: Session = Depends(get_db)):
    existing_email = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="the email you entered is already used",
        )
    hashed_password = hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the database is empty (there is no user)",
        )
    return users


@router.get("/{id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the user with the id {id} can not be found",
        )
    return user


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exist",
        )
    db.delete(user)
    db.commit()
    return {f"user with id :{id} is successfully deleted"}
