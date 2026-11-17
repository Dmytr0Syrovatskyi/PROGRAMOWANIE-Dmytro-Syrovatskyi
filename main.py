import csv
import os

from fastapi import FastAPI, HTTPException

from models import Link, Movie, Rating, Tag

app = FastAPI(title="Movies REST API")
DATA_DIR = "data"


def read_csv_rows(filename: str) -> list[dict[str, str]]:
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail=f"Plik {filename} nie został znaleziony w katalogu {DATA_DIR}/",
        )
    with open(filepath, mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.get("/movies")
def get_movies():
    rows = read_csv_rows("movies.csv")
    movies = [
        Movie(id=row["movieId"], title=row["title"], genres=row["genres"])
        for row in rows
    ]
    return [movie.__dict__ for movie in movies]


@app.get("/links")
def get_links():
    rows = read_csv_rows("links.csv")
    links = [
        Link(
            movieId=row["movieId"],
            imdbId=row["imdbId"],
            tmdbId=row["tmdbId"],
        )
        for row in rows
    ]
    return [link.__dict__ for link in links]


@app.get("/ratings")
def get_ratings():
    rows = read_csv_rows("ratings.csv")
    ratings = [
        Rating(
            userId=row["userId"],
            movieId=row["movieId"],
            rating=row["rating"],
            timestamp=row["timestamp"],
        )
        for row in rows
    ]
    return [rating.__dict__ for rating in ratings]


@app.get("/tags")
def get_tags():
    rows = read_csv_rows("tags.csv")
    tags = [
        Tag(
            userId=row["userId"],
            movieId=row["movieId"],
            tag=row["tag"],
            timestamp=row["timestamp"],
        )
        for row in rows
    ]
    return [tag.__dict__ for tag in tags]