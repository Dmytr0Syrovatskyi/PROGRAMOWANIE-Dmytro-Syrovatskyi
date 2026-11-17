import time
from fastapi.testclient import TestClient
import requests

# Importujemy nasze aplikacje FastAPI
from service_a.main import app as app_a
from service_b.main import app as app_b

client_a = TestClient(app_a)
client_b = TestClient(app_b)


# ==========================================
# PUNKT 8: Testy integracyjne endpointów
# ==========================================
def test_service_a_integration():
    # 1. Test zapisu danych w Serwisie A
    payload = {"id": "test-123", "people_count": 5}
    response_post = client_a.post("/save_result", json=payload)

    assert response_post.status_code == 200
    assert response_post.json()["status"] == "success"
    assert response_post.json()["id"] == "test-123"

    # 2. Test odczytu danych w Serwisie A
    response_get = client_a.get("/result/test-123")
    assert response_get.status_code == 200
    assert response_get.json()["people_count"] == 5
    assert response_get.json()["status"] == "done"


def test_service_b_integration():
    # Test czy Serwis B poprawnie przyjmuje zadanie i odkłada do kolejki
    # Wymaga działającego RabbitMQ w tle
    test_url = (
        "https://raw.githubusercontent.com/pjreddie/darknet/master/data/person.jpg"
    )
    response = client_b.post(f"/analyze?url={test_url}")

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["message"] == "Task queued successfully"


# ==========================================
# PUNKT 9: Testy E2E (End-to-End)
# ==========================================
def test_e2e_communication():
    """
    Test E2E sprawdza pełen przepływ informacji:
    Serwis B -> RabbitMQ -> Worker (Docker) -> Serwis A
    UWAGA: Wymaga uruchomionych wszystkich serwisów (A, B oraz workerów z RabbitMQ).
    """
    test_url = (
        "https://raw.githubusercontent.com/pjreddie/darknet/master/data/person.jpg"
    )

    # 1. Wysyłamy żądanie do działającego Serwisu B (port 8000)
    response = requests.post(f"http://127.0.0.1:8000/analyze?url={test_url}")
    assert response.status_code == 200
    task_id = response.json()["id"]

    # 2. Czekamy 5 sekund, aby worker miał czas na pobranie obrazu,
    # przetworzenie go przez model AI i wysłanie wyniku do Serwisu A.
    time.sleep(5)

    # 3. Sprawdzamy, czy wynik dotarł do Serwisu A (port 8001)
    response_check = requests.get(f"http://127.0.0.1:8001/result/{task_id}")
    assert response_check.status_code == 200

    data = response_check.json()
    assert data["status"] == "done"
    assert data["people_count"] >= 0