from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import Link, Movie, Rating, Tag


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_data(db_session):
    movies = [
        Movie(id=1, title="Toy Story (1995)", genres="Adventure|Animation"),
        Movie(id=2, title="Jumanji (1995)", genres="Adventure|Children"),
    ]
    links = [
        Link(movieId=1, imdbId="0114709", tmdbId="862"),
        Link(movieId=2, imdbId="0113497", tmdbId="8844"),
    ]
    ratings = [
        Rating(id=1, userId=1, movieId=1, rating=4.0, timestamp=964982703),
        Rating(id=2, userId=1, movieId=2, rating=5.0, timestamp=964981247),
    ]
    tags = [
        Tag(id=1, userId=2, movieId=1, tag="pixar", timestamp=1445714994),
        Tag(id=2, userId=2, movieId=2, tag="magic", timestamp=1445715207),
    ]
    db_session.add_all(movies + links + ratings + tags)
    db_session.commit()


# ==================== MOVIES TESTS ====================
def test_get_movies_list(client, seed_data):
    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Toy Story (1995)"


def test_get_movie_item(client, seed_data):
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["genres"] == "Adventure|Animation"

    not_found = client.get("/movies/999")
    assert not_found.status_code == 404


def test_create_movie(client, seed_data):
    payload = {"id": 3, "title": "Heat (1995)", "genres": "Action|Crime"}
    response = client.post("/movies", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Heat (1995)"

    check = client.get("/movies")
    assert len(check.json()) == 3


def test_update_movie(client, seed_data):
    payload = {"title": "Toy Story Updated", "genres": "Animation|Comedy"}
    response = client.put("/movies/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Toy Story Updated"

    check = client.get("/movies/1")
    assert check.json()["genres"] == "Animation|Comedy"
    assert client.put("/movies/999", json=payload).status_code == 404


def test_delete_movie(client, seed_data):
    response = client.delete("/movies/1")
    assert response.status_code == 200
    assert client.get("/movies/1").status_code == 404
    assert client.delete("/movies/1").status_code == 404


# ==================== LINKS TESTS ====================
def test_get_links_list(client, seed_data):
    response = client.get("/links")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_link_item(client, seed_data):
    response = client.get("/links/1")
    assert response.status_code == 200
    assert response.json()["imdbId"] == "0114709"
    assert client.get("/links/999").status_code == 404


def test_create_link(client, seed_data):
    payload = {"movieId": 3, "imdbId": "0113277", "tmdbId": "949"}
    response = client.post("/links", json=payload)
    assert response.status_code == 201
    assert response.json()["movieId"] == 3
    assert len(client.get("/links").json()) == 3


def test_update_link(client, seed_data):
    payload = {"imdbId": "9999999", "tmdbId": "1111"}
    response = client.put("/links/1", json=payload)
    assert response.status_code == 200
    assert response.json()["imdbId"] == "9999999"
    assert client.put("/links/999", json=payload).status_code == 404


def test_delete_link(client, seed_data):
    response = client.delete("/links/1")
    assert response.status_code == 200
    assert client.get("/links/1").status_code == 404
    assert client.delete("/links/1").status_code == 404


# ==================== RATINGS TESTS ====================
def test_get_ratings_list(client, seed_data):
    response = client.get("/ratings")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_rating_item(client, seed_data):
    response = client.get("/ratings/1")
    assert response.status_code == 200
    assert response.json()["rating"] == 4.0
    assert client.get("/ratings/999").status_code == 404


def test_create_rating(client, seed_data):
    payload = {
        "userId": 2,
        "movieId": 1,
        "rating": 3.5,
        "timestamp": 1000000000,
    }
    response = client.post("/ratings", json=payload)
    assert response.status_code == 201
    assert response.json()["rating"] == 3.5
    assert len(client.get("/ratings").json()) == 3


def test_update_rating(client, seed_data):
    payload = {
        "userId": 1,
        "movieId": 1,
        "rating": 5.0,
        "timestamp": 1000000005,
    }
    response = client.put("/ratings/1", json=payload)
    assert response.status_code == 200
    assert response.json()["rating"] == 5.0
    assert client.put("/ratings/999", json=payload).status_code == 404


def test_delete_rating(client, seed_data):
    response = client.delete("/ratings/1")
    assert response.status_code == 200
    assert client.get("/ratings/1").status_code == 404
    assert client.delete("/ratings/1").status_code == 404


# ==================== TAGS TESTS ====================
def test_get_tags_list(client, seed_data):
    response = client.get("/tags")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_tag_item(client, seed_data):
    response = client.get("/tags/1")
    assert response.status_code == 200
    assert response.json()["tag"] == "pixar"
    assert client.get("/tags/999").status_code == 404


def test_create_tag(client, seed_data):
    payload = {
        "userId": 3,
        "movieId": 1,
        "tag": "classic",
        "timestamp": 1500000000,
    }
    response = client.post("/tags", json=payload)
    assert response.status_code == 201
    assert response.json()["tag"] == "classic"
    assert len(client.get("/tags").json()) == 3


def test_update_tag(client, seed_data):
    payload = {
        "userId": 2,
        "movieId": 1,
        "tag": "disney-pixar",
        "timestamp": 1500000010,
    }
    response = client.put("/tags/1", json=payload)
    assert response.status_code == 200
    assert response.json()["tag"] == "disney-pixar"
    assert client.put("/tags/999", json=payload).status_code == 404


def test_delete_tag(client, seed_data):
    response = client.delete("/tags/1")
    assert response.status_code == 200
    assert client.get("/tags/1").status_code == 404
    assert client.delete("/tags/1").status_code == 404