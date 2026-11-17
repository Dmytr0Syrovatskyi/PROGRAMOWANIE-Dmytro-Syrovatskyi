from typing import Optional

from pydantic import BaseModel, ConfigDict


class MovieCreate(BaseModel):
    id: Optional[int] = None
    title: str
    genres: str


class MovieUpdate(BaseModel):
    title: str
    genres: str


class MovieOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    genres: str


class LinkCreate(BaseModel):
    movieId: Optional[int] = None
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None


class LinkUpdate(BaseModel):
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None


class LinkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movieId: int
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None


class RatingCreate(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


class RatingUpdate(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


class RatingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    userId: int
    movieId: int
    rating: float
    timestamp: int


class TagCreate(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


class TagUpdate(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    userId: int
    movieId: int
    tag: str
    timestamp: int