"""
Zadanie 2:
Funkcja przyjmująca dwa argumenty typu int i zwracająca wynik ich mnożenia.
"""


def pomnoz(a: int, b: int) -> int:
    # Zwracamy iloczyn obu liczb
    return a * b


if __name__ == "__main__":
    # Uruchomienie funkcji i bezpośrednie wyświetlenie wyniku
    print(pomnoz(4, 5))