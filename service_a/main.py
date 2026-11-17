from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Service A - Results Storage")


# Model danych, które otrzymujemy od konsumenta (Workera)
class ResultPayload(BaseModel):
    id: str
    people_count: int


# Prosta baza danych w pamięci (słownik) do przechowywania wyników
results_db: Dict[str, int] = {}


@app.post("/save_result")
def save_result(payload: ResultPayload):
    # Zapisywanie wyniku w pamięci
    results_db[payload.id] = payload.people_count
    return {"status": "success", "id": payload.id}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    # Endpoint pozwalający sprawdzić, czy analiza została zakończona
    if task_id in results_db:
        return {
            "id": task_id,
            "status": "done",
            "people_count": results_db[task_id],
        }
    return {"id": task_id, "status": "pending"}