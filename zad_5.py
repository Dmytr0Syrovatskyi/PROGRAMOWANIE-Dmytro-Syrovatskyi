"""
Zadanie 5:
Funkcja sprawdzająca (bool),
czy podana liczba (int) znajduje się w liście (list).
"""


def sprawdz_zawartosc(lista: list, wartosc: int) -> bool:
    # Operator 'in' weryfikuje, czy wartość zawiera się w obiekcie
    return wartosc in lista


if __name__ == "__main__":
    moja_lista = [10, 20, 30, 40]

    # Wyświetli True, ponieważ 30 znajduje się w liście
    print(sprawdz_zawartosc(moja_lista, 30))