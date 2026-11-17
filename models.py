from sqlalchemy import Column, Float, Integer, String

from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=False)


class Link(Base):
    __tablename__ = "links"

    movieId = Column(Integer, primary_key=True, index=True)
    imdbId = Column(String, nullable=True)
    tmdbId = Column(String, nullable=True)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, index=True, nullable=False)
    movieId = Column(Integer, index=True, nullable=False)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, index=True, nullable=False)
    movieId = Column(Integer, index=True, nullable=False)
    tag = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)