from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine, get_db
from .routes import users, posts, login,votes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(login.router)
app.include_router(votes.router)


@app.get("/")
def home(db: Session = Depends(get_db)):
    return {"detail": "welcome to the home page"}
