from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Link, Movie, Rating, Tag
from schemas import (
    LinkCreate,
    LinkOut,
    LinkUpdate,
    MovieCreate,
    MovieOut,
    MovieUpdate,
    RatingCreate,
    RatingOut,
    RatingUpdate,
    TagCreate,
    TagOut,
    TagUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movies REST API - CRUD")


@app.get("/")
def hello_world():
    return {"hello": "world"}


# ==================== MOVIES ====================
@app.get("/movies", response_model=list[MovieOut])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Movie).offset(skip).limit(limit).all()


@app.post(
    "/movies", response_model=MovieOut, status_code=status.HTTP_201_CREATED
)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    if payload.id is not None:
        existing = db.query(Movie).filter(Movie.id == payload.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Movie ID already exists")
    movie = Movie(**payload.model_dump(exclude_none=True))
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.put("/movies/{movie_id}", response_model=MovieOut)
def update_movie(
    movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.title = payload.title
    movie.genres = payload.genres
    db.commit()
    db.refresh(movie)
    return movie


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"detail": "Movie deleted"}


# ==================== LINKS ====================
@app.get("/links", response_model=list[LinkOut])
def get_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Link).offset(skip).limit(limit).all()


@app.post("/links", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
def create_link(payload: LinkCreate, db: Session = Depends(get_db)):
    if payload.movieId is not None:
        existing = (
            db.query(Link).filter(Link.movieId == payload.movieId).first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Link movieId already exists")
    link = Link(**payload.model_dump(exclude_none=True))
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@app.get("/links/{movie_id}", response_model=LinkOut)
def get_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.put("/links/{movie_id}", response_model=LinkOut)
def update_link(
    movie_id: int, payload: LinkUpdate, db: Session = Depends(get_db)
):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    link.imdbId = payload.imdbId
    link.tmdbId = payload.tmdbId
    db.commit()
    db.refresh(link)
    return link


@app.delete("/links/{movie_id}")
def delete_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return {"detail": "Link deleted"}


# ==================== RATINGS ====================
@app.get("/ratings", response_model=list[RatingOut])
def get_ratings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Rating).offset(skip).limit(limit).all()


@app.post(
    "/ratings", response_model=RatingOut, status_code=status.HTTP_201_CREATED
)
def create_rating(payload: RatingCreate, db: Session = Depends(get_db)):
    rating = Rating(**payload.model_dump())
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


@app.get("/ratings/{rating_id}", response_model=RatingOut)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@app.put("/ratings/{rating_id}", response_model=RatingOut)
def update_rating(
    rating_id: int, payload: RatingUpdate, db: Session = Depends(get_db)
):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    rating.userId = payload.userId
    rating.movieId = payload.movieId
    rating.rating = payload.rating
    rating.timestamp = payload.timestamp
    db.commit()
    db.refresh(rating)
    return rating


@app.delete("/ratings/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    db.delete(rating)
    db.commit()
    return {"detail": "Rating deleted"}


# ==================== TAGS ====================
@app.get("/tags", response_model=list[TagOut])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Tag).offset(skip).limit(limit).all()


@app.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
    tag = Tag(**payload.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.get("/tags/{tag_id}", response_model=TagOut)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.put("/tags/{tag_id}", response_model=TagOut)
def update_tag(tag_id: int, payload: TagUpdate, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag.userId = payload.userId
    tag.movieId = payload.movieId
    tag.tag = payload.tag
    tag.timestamp = payload.timestamp
    db.commit()
    db.refresh(tag)
    return tag


@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"detail": "Tag deleted"}