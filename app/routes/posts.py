from fastapi import APIRouter, status, Depends, HTTPException, Response
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List
from ..oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    print(current_user.email)
    return db_post


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="you can not access either because the database is empty or because you don't have these posts",
        )
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    post = (
        db.query(models.Post)
        .filter((models.Post.id == id) & (models.Post.owner_id == current_user.id))
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with id : {id} does not exist ",
        )
    return post


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query_post = db.query(models.Post).filter(
        (models.Post.id == id) & (models.Post.owner_id == current_user.id)
    )
    if not query_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} does not exist",
        )
    query_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return query_post.first()


@router.delete("/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = (
        db.query(models.Post)
        .filter((models.Post.id == id) & (models.Post.owner_id == current_user.id))
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} does not exist ",
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)
