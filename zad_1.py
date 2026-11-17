"""
Zadanie 1:
Funkcja przyjmująca dwa parametry typu string i zwracająca string z powitaniem.
"""


def powitanie(name: str, surname: str) -> str:
    # Wykorzystujemy f-string do formatowania tekstu
    return f"Cześć {name} {surname}!"


if __name__ == "__main__":
    # Uruchomienie funkcji i zapisanie wyniku do zmiennej
    wynik = powitanie("Jan", "Kowalski")

    # Wyświetlenie zapisanego wyniku
    print(wynik)