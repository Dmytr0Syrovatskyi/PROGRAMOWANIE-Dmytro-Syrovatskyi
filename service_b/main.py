import json
import os
import uuid
from fastapi import FastAPI
import pika

app = FastAPI(title="Service B - AI Producer")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "ai_tasks"


@app.post("/analyze")
def analyze_image(url: str):
    task_id = uuid.uuid4().hex

    # Nawiązanie połączenia z serwerem RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )
    channel = connection.channel()

    # durable=True oznacza, że kolejka przetrwa restart serwera
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    message = {"id": task_id, "url": url}

    # Wysłanie zadania do kolejki (Producer)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # wiadomości zapisywane na dysku
        ),
    )
    connection.close()

    return {"message": "Task queued successfully", "id": task_id}