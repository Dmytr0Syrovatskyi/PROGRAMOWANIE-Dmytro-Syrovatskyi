import csv
import os
import uuid

FILENAME = 'queue.csv'


def add_task():
    # Tworzy plik z nagłówkami, jeśli jeszcze nie istnieje
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["task_id", "status"])

    # Generowanie unikalnego ID dla każdego zgłoszenia/rozmowy
    task_id = str(uuid.uuid4())[:8]

    # Zapis zadania ze statusem pending
    with open(FILENAME, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([task_id, "pending"])

    print(f"Producent: Dodano zadanie '{task_id}' ze statusem 'pending'.")


if __name__ == "__main__":
    add_task()