from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Link, Movie, Rating, Tag

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movies REST API (SQLite + SQLAlchemy)")


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.get("/movies")
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Movie).offset(skip).limit(limit).all()


@app.get("/links")
def get_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Link).offset(skip).limit(limit).all()


@app.get("/ratings")
def get_ratings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Rating).offset(skip).limit(limit).all()


@app.get("/tags")
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Tag).offset(skip).limit(limit).all()