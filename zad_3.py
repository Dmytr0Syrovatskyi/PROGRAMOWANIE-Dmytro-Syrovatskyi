"""
Zadanie 3:
Dziedziczenie klas. Klasa bazowa Property oraz klasy pochodne House i Flat.
"""


class Property:
    def __init__(self, area: float, rooms: int, price: float, address: str):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address


class House(Property):
    def __init__(
        self, area: float, rooms: int, price: float, address: str, plot: int
    ):
        # Wywołanie konstruktora klasy bazowej (Property)
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self) -> str:
        return (
            f"Dom: {self.address} | Powierzchnia: {self.area} m2 | "
            f"Pokoje: {self.rooms} | Działka: {self.plot} m2 | "
            f"Cena: {self.price} PLN"
        )


class Flat(Property):
    def __init__(
        self, area: float, rooms: int, price: float, address: str, floor: int
    ):
        # Wywołanie konstruktora klasy bazowej (Property)
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self) -> str:
        return (
            f"Mieszkanie: {self.address} | Piętro: {self.floor} | "
            f"Powierzchnia: {self.area} m2 | Pokoje: {self.rooms} | "
            f"Cena: {self.price} PLN"
        )


if __name__ == "__main__":
    # Tworzenie obiektu House
    moj_dom = House(
        area=150.5,
        rooms=5,
        price=1200000.0,
        address="Kwiatowa 12, Poznań",
        plot=800,
    )

    # Tworzenie obiektu Flat
    moje_mieszkanie = Flat(
        area=55.0,
        rooms=2,
        price=650000.0,
        address="Długa 5/10, Gdańsk",
        floor=3,
    )

    # Wyświetlanie
    print(moj_dom)
    print(moje_mieszkanie)