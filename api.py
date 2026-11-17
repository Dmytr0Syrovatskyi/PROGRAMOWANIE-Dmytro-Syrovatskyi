import glob
import json
import os
import uuid
from fastapi import FastAPI
import pika

app = FastAPI()
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'image_tasks'

os.makedirs("analyzed", exist_ok=True)


@app.post("/analyze_img")
def analyze_img(url: str):
    task_id = uuid.uuid4().hex

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    message = {'id': task_id, 'url': url}
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
    )
    connection.close()

    return {"message": "Zadanie dodane do kolejki", "id": task_id}


@app.get("/check")
def check_status(id: str):
    files = glob.glob(f"analyzed/{id}-*.*")

    if not files:
        return {"status": "W kolejce lub przetwarzane (pending)"}

    filename = os.path.basename(files[0])
    number_with_ext = filename.replace(f"{id}-", "")
    detected_people = number_with_ext.split('.')[0]

    return {
        "status": "Zakończono (done)",
        "id": id,
        "detected_people": int(detected_people),
    }