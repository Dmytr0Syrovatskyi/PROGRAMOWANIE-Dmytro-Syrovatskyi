import json
import os
import cv2
import numpy as np
import pika
import requests

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'image_tasks'
os.makedirs("analyzed", exist_ok=True)


def detect_people(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    boxes, weights = hog.detectMultiScale(img, winStride=(8, 8))
    return len(boxes), img


def callback(ch, method, properties, body):
    data = json.loads(body)
    task_id = data['id']
    url = data['url']

    print(f"Rozpoczęto analizę: {task_id}...")

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        people_count, img = detect_people(response.content)

        filename = f"analyzed/{task_id}-{people_count}.jpg"
        cv2.imwrite(filename, img)

        print(
            f"Zakończono! Zapisano jako {filename}. "
            f"Znaleziono osób: {people_count}"
        )

    except Exception as e:
        print(f"Błąd przetwarzania {task_id}: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("Konsument uruchomiony. Oczekuję na obrazy do analizy...")
    channel.start_consuming()