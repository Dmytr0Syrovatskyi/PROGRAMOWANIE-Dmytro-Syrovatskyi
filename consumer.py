import sqlite3
import time

DB_NAME = 'queue.db'


def consume():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Zabezpieczenie na wypadek, gdyby konsument uruchomił się przed producentem
    cursor.execute('''CREATE TABLE IF NOT EXISTS queue (
                        task_id TEXT PRIMARY KEY,
                        status TEXT
                    )''')
    conn.commit()

    print("Konsument uruchomiony. Oczekuję na zadania...")

    while True:
        # 1. Szukamy zadania ze statusem 'pending'
        cursor.execute("SELECT task_id FROM queue WHERE status = 'pending' LIMIT 1")
        row = cursor.fetchone()

        if row:
            task_id = row[0]

            # 2. Próbujemy zmienić status na 'in_progress'.
            # Dodatkowy warunek WHERE status = 'pending' zapobiega konfliktom, gdyby inny konsument ubiegł nas w ułamku sekundy.
            cursor.execute(
                "UPDATE queue SET status = 'in_progress' WHERE task_id = ? AND status = 'pending'",
                (task_id,),
            )
            conn.commit()

            # Sprawdzamy, czy udało się zaktualizować wiersz
            if cursor.rowcount > 0:
                print(f"Konsument: Pobrano zadanie '{task_id}'. Zmieniono status na 'in_progress'.")
                print(f"Konsument: Wykonuję pracę '{task_id}'... (potrwa to 30s)")

                # 3. Symulacja pracy operatora
                time.sleep(30)

                # 4. Zakończenie pracy i zmiana statusu na 'done'
                cursor.execute(
                    "UPDATE queue SET status = 'done' WHERE task_id = ?",
                    (task_id,),
                )
                conn.commit()

                print(f"Konsument: Zadanie '{task_id}' zakończone. Status zmieniono na 'done'.")
            else:
                # Inny konsument zabrał to zadanie szybciej, próbujemy ponownie natychmiast
                continue
        else:
            # Jeśli nie ma żadnych zadań 'pending', czekamy 5 sekund
            print("Brak zadań 'pending'. Czekam 5s...")
            time.sleep(5)


if __name__ == "__main__":
    consume()