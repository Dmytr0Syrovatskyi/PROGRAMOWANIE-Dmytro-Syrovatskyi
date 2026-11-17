from magazine import utils


class Order:
    def __init__(self, order_id: int):
        self.order_id = order_id
        print(f"Utworzono zamówienie nr: {self.order_id}")
        # Wywołanie funkcji z zaimportowanego modułu utils
        utils.pomocnicza_funkcja()