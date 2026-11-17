import csv
import os

from database import Base, SessionLocal, engine
from models import Link, Movie, Rating, Tag

DATA_DIR = "data"


def read_csv(filename: str) -> list[dict[str, str]]:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_all_data() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(Movie).first() is None:
            movies = [
                Movie(
                    id=int(row["movieId"]),
                    title=row["title"],
                    genres=row["genres"],
                )
                for row in read_csv("movies.csv")
            ]
            db.bulk_save_objects(movies)
            print(f"Załadowano {len(movies)} rekordów do tabeli 'movies'.")

        if db.query(Link).first() is None:
            links = [
                Link(
                    movieId=int(row["movieId"]),
                    imdbId=row["imdbId"] or None,
                    tmdbId=row["tmdbId"] or None,
                )
                for row in read_csv("links.csv")
            ]
            db.bulk_save_objects(links)
            print(f"Załadowano {len(links)} rekordów do tabeli 'links'.")

        if db.query(Rating).first() is None:
            ratings = [
                Rating(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"]),
                )
                for row in read_csv("ratings.csv")
            ]
            db.bulk_save_objects(ratings)
            print(f"Załadowano {len(ratings)} rekordów do tabeli 'ratings'.")

        if db.query(Tag).first() is None:
            tags = [
                Tag(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    tag=row["tag"],
                    timestamp=int(row["timestamp"]),
                )
                for row in read_csv("tags.csv")
            ]
            db.bulk_save_objects(tags)
            print(f"Załadowano {len(tags)} rekordów do tabeli 'tags'.")

        db.commit()
        print("Baza danych SQLite została pomyślnie zasilona danymi!")
    finally:
        db.close()


if __name__ == "__main__":
    load_all_data()