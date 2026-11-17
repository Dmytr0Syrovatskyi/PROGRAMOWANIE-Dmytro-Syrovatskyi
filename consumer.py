import csv
import os
import time

FILENAME = 'queue.csv'


# Funkcje pomocnicze omijające problem jednoczesnego dostępu do pliku przez wielu konsumentów
def read_queue():
    while True:
        try:
            with open(FILENAME, mode='r', newline='', encoding='utf-8') as f:
                return list(csv.reader(f))
        except PermissionError:
            time.sleep(0.1)  # Jeśli plik jest zablokowany, spróbuj za ułamek sekundy


def write_queue(data):
    while True:
        try:
            with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            break
        except PermissionError:
            time.sleep(0.1)


def consume():
    print("Konsument uruchomiony. Oczekuję na zadania...")
    while True:
        if not os.path.exists(FILENAME):
            time.sleep(5)
            continue

        tasks = read_queue()

        task_found = False
        task_id = None

        # Szukanie pierwszego zadania ze statusem 'pending'
        for i in range(1, len(tasks)):
            if tasks[i][1] == "pending":
                task_found = True
                task_id = tasks[i][0]
                tasks[i][1] = "in_progress"  # Zmiana statusu
                break

        if task_found:
            # Zapisujemy status in_progress do pliku, by inni konsumenci tego nie wzięli
            write_queue(tasks)

            print(f"Konsument: Pobrano zadanie '{task_id}'. Zmieniono status na 'in_progress'.")

            # Symulacja pracy trwającej 30 sekund
            print(f"Konsument: Wykonuję pracę '{task_id}'... (potrwa to 30s)")
            time.sleep(30)

            # Ponowne wczytanie pliku (inni konsumenci mogli dopisać/zmienić inne wiersze przez te 30s)
            tasks = read_queue()
            for i in range(1, len(tasks)):
                if tasks[i][0] == task_id:
                    tasks[i][1] = "done"  # Zmiana statusu po wykonaniu
                    break

            write_queue(tasks)
            print(f"Konsument: Zadanie '{task_id}' zakończone. Status zmieniono na 'done'.")
        else:
            # Jeśli nie znaleziono pracy, czeka 5 sekund
            print("Brak zadań 'pending'. Czekam 5s...")
            time.sleep(5)


if __name__ == "__main__":
    consume()