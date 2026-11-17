"""
Zadanie 4:
Funkcja przyjmująca 3 liczby (int).
Sprawdza, czy suma dwóch pierwszych jest >= trzeciej.
"""


def sprawdz_sume(a: int, b: int, c: int) -> bool:
    # Wyrażenie (a + b) >= c automatycznie zwraca True lub False
    return (a + b) >= c


if __name__ == "__main__":
    # Przykładowe wywołanie funkcji: 5+5=10, co jest >= 8 (zwróci True)
    print(sprawdz_sume(5, 5, 8))