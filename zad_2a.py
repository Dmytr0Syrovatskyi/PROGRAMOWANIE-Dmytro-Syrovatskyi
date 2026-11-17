"""
Zadanie 2a:
Funkcja przyjmująca listę 5 imion i wyświetlająca każde z nich.
"""


def wyswietl_imiona(lista_imion):
    # Pętla przechodząca przez każdy element listy
    for imie in lista_imion:
        print(imie)


if __name__ == "__main__":
    # Deklaracja zmiennej z listą 5 imion
    moje_imiona = ["Martin", "Tom", "Eva", "Kasia", "Piotr"]

    # Wywołanie funkcji
    wyswietl_imiona(moje_imiona)