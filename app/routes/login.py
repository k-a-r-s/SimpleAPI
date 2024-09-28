from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(tags=["login"], prefix="/login")


@router.post("/", response_model=schemas.Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )

    if not verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )

    access_token = create_access_token({"username": user.email,"id":user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
