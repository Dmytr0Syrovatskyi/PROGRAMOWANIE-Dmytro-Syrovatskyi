"""
Zadanie 6:
Funkcja łącząca dwie listy, usuwająca duplikaty i podnosząca do potęgi 3.
"""


def polacz_i_poteguj(lista1: list, lista2: list) -> list:
    # 1. Łączymy listy (lista1 + lista2)
    # 2. Rzutujemy na 'set', aby usunąć duplikaty
    # 3. Rzutujemy z powrotem na 'list'
    unikalne = list(set(lista1 + lista2))

    # Lista składana podnosząca każdy element do potęgi 3 (** 3)
    return [x**3 for x in unikalne]


if __name__ == "__main__":
    l1 = [1, 2, 3]
    l2 = [2, 3, 4]  # Wartości 2 i 3 się powtarzają

    print(polacz_i_poteguj(l1, l2))