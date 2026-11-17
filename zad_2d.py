"""
Zadanie 2d:
Funkcja przyjmująca 10 liczb (z użyciem range)
i wyświetlająca co drugi element.
"""


def wyswietl_co_drugi(liczby):
    # Wykorzystanie wycinków (slicing) w formacie [start:stop:step]
    # Krok 2 oznacza pomijanie co drugiego elementu
    for liczba in liczby[::2]:
        print(liczba)


if __name__ == "__main__":
    # Generowanie listy 10 liczb (od 0 do 9) za pomocą range
    dziesiec_liczb = list(range(10))
    wyswietl_co_drugi(dziesiec_liczb)