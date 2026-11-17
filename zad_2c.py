"""
Zadanie 2c:
Funkcja przyjmująca 10 liczb (z użyciem range)
i wyświetlająca tylko parzyste elementy.
"""


def wyswietl_parzyste(liczby):
    for liczba in liczby:
        # Sprawdzamy resztę z dzielenia (modulo), aby ustalić parzystość
        if liczba % 2 == 0:
            print(liczba)


if __name__ == "__main__":
    # Generowanie listy 10 liczb (od 0 do 9) za pomocą range
    dziesiec_liczb = list(range(10))
    wyswietl_parzyste(dziesiec_liczb)