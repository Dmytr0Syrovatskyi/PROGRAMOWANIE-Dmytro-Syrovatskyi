"""
Zadanie 2b:
Funkcja mnożąca elementy listy przez 2 w dwóch wersjach:
i. Z wykorzystaniem pętli for
ii. Z wykorzystaniem listy składanej (list comprehension)
"""


# Wersja i: pętla for
def pomnoz_for(liczby):
    wynik = []  # Pusta lista na wyniki
    for liczba in liczby:
        wynik.append(liczba * 2)
    return wynik


# Wersja ii: lista składana
def pomnoz_skladana(liczby):
    return [liczba * 2 for liczba in liczby]


if __name__ == "__main__":
    moje_liczby = [1, 2, 3, 4, 5]

    # Wyświetlenie wyników z obu funkcji
    print("Pętla for:", pomnoz_for(moje_liczby))
    print("Lista składana:", pomnoz_skladana(moje_liczby))