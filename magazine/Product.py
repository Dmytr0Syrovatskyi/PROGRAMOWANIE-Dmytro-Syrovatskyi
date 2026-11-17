from magazine import utils


class Product:
    def __init__(self, name: str):
        self.name = name
        print(f"Utworzono produkt: {self.name}")
        # Wywołanie funkcji z zaimportowanego modułu utils
        utils.pomocnicza_funkcja()