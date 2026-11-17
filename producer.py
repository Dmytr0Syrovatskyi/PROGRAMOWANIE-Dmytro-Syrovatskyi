import sqlite3
import uuid

DB_NAME = 'queue.db'


def add_task():
    # Połączenie z bazą danych (tworzy plik, jeśli nie istnieje)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tworzenie tabeli, jeśli jeszcze nie istnieje
    cursor.execute('''CREATE TABLE IF NOT EXISTS queue (
                        task_id TEXT PRIMARY KEY,
                        status TEXT
                    )''')

    # Generowanie unikalnego ID i zapis do bazy
    task_id = str(uuid.uuid4())[:8]
    cursor.execute(
        "INSERT INTO queue (task_id, status) VALUES (?, ?)",
        (task_id, "pending"),
    )

    # Zatwierdzenie zmian (commit) i zamknięcie połączenia
    conn.commit()
    conn.close()

    print(f"Producent: Dodano zadanie '{task_id}' ze statusem 'pending'.")


if __name__ == "__main__":
    add_task()