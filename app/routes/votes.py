from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Vote
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models, schemas
from typing import List

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"you dont have access to the post wih id : {vote.post_id}",
        )
    vote_query = db.query(models.Vote).filter(
        (models.Vote.post_id == vote.post_id) & (models.Vote.user_id == current_user.id)
    )

    search_vote = vote_query.first()
    if vote.dir == 1:
        if search_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"the post that you trying to vote to is already voted <3",
            )
        else:
            db_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(db_vote)
            db.commit()
            return {"message": "The vote is successfully added"}
    else:
        if not search_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"cannot find the post with id : {vote.post_id}",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"detail": "The vote is successfully deleted"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Votes_out])
def get_votes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    votes = db.query(models.Vote).all()
    if not votes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is not votes in the current time",
        )

    return votes


@router.get(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=List[schemas.Vote_out]
)
def get_post_votes(
    post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    votes = db.query(models.Vote).filter(models.Vote.post_id == post_id).all()
    
    if not votes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No votes found for post with id: {post_id}",
        )

    return votes
