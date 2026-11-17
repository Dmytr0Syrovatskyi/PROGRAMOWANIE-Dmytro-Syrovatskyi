"""
Zadanie 3:
Funkcja sprawdzająca parzystość liczby. Zwraca typ logiczny bool.
"""


def czy_parzysta(liczba: int) -> bool:
    # Używamy operatora modulo (%), reszta z dzielenia przez 2 musi wynosić 0
    return liczba % 2 == 0


if __name__ == "__main__":
    # Zapisanie wyniku do zmiennej
    wynik = czy_parzysta(8)

    # Warunek logiczny sprawdzający wartość zmiennej 'wynik'
    if wynik:
        print("Liczba parzysta")
    else:
        print("Liczba nieparzysta")