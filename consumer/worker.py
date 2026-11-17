import json
import os
import time
import cv2
import numpy as np
import pika
import requests

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
SERVICE_A_URL = os.getenv(
    "SERVICE_A_URL", "http://host.docker.internal:8001/save_result"
)
QUEUE_NAME = "ai_tasks"


def detect_people(image_bytes: bytes) -> int:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Nie udało się zdekodować obrazu.")

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    boxes, _ = hog.detectMultiScale(img, winStride=(8, 8))
    return len(boxes)


def callback(ch, method, properties, body):
    data = json.loads(body)
    task_id = data["id"]
    url = data["url"]

    print(f"[Worker] Przetwarzanie zadania {task_id} z URL: {url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        img_response = requests.get(url, headers=headers, timeout=15)
        img_response.raise_for_status()

        people_count = detect_people(img_response.content)

        # Wysyłanie wyniku do Serwisu A (odporne na przestoje / Cloudflare)
        payload = {"id": task_id, "people_count": people_count}
        res = requests.post(SERVICE_A_URL, json=payload, timeout=10)
        res.raise_for_status()

        print(f"[Worker] Sukces {task_id}: wykryto {people_count} osób.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except requests.RequestException as exc:
        # Retry strategy: brak ACK + requeue=True zwraca wiadomość do kolejki
        print(f"[Worker] Błąd połączenia dla {task_id}: {exc}. Ponawiam za 5s...")
        time.sleep(5)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    except Exception as exc:
        print(f"[Worker] Błąd krytyczny obrazu {task_id}: {exc}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback,
                auto_ack=False,
            )
            print("[Worker] Połączono z RabbitMQ. Oczekiwanie na zadania...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("[Worker] RabbitMQ niedostępny, ponowna próba za 5s...")
            time.sleep(5)


if __name__ == "__main__":
    start_worker()