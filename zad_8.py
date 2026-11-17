"""
Zadanie 8:
Skrypt korzystający z modułu argparse do filtrowania pobieranych browarów
na podstawie parametru --city przekazanego w terminalu.
"""

import argparse
from typing import Optional
import requests


class Brewery:
    def __init__(
        self,
        id: str,
        name: str,
        brewery_type: str,
        address_1: Optional[str],
        city: Optional[str],
        state_province: Optional[str],
        postal_code: Optional[str],
        country: Optional[str],
        longitude: Optional[str],
        latitude: Optional[str],
        phone: Optional[str],
        website_url: Optional[str],
    ) -> None:
        self.id: str = id
        self.name: str = name
        self.brewery_type: str = brewery_type
        self.address_1: Optional[str] = address_1
        self.city: Optional[str] = city
        self.state_province: Optional[str] = state_province
        self.postal_code: Optional[str] = postal_code
        self.country: Optional[str] = country
        self.longitude: Optional[str] = longitude
        self.latitude: Optional[str] = latitude
        self.phone: Optional[str] = phone
        self.website_url: Optional[str] = website_url

    def __str__(self) -> str:
        return (
            f"Browar: {self.name} | Typ: {self.brewery_type} | "
            f"Miasto: {self.city} | WWW: {self.website_url}"
        )


def main() -> None:
    # Wczytywanie przekazywanych parametrów
    parser = argparse.ArgumentParser(
        description="Pobieranie informacji o browarach z API"
    )
    parser.add_argument(
        "--city",
        type=str,
        help="Filtruj browary po mieście (np. --city=Berlin)",
    )
    args = parser.parse_args()

    url = "https://api.openbrewerydb.org/v1/breweries?per_page=20"

    # Dodanie parametru do adresu API, jeśli został podany w konsoli
    if args.city:
        url += f"&by_city={args.city}"

    response = requests.get(url)
    response.raise_for_status()
    dane = response.json()

    lista_browarow: list = []

    for b in dane:
        obiekt_brewery = Brewery(
            id=b.get("id", ""),
            name=b.get("name", "Brak nazwy"),
            brewery_type=b.get("brewery_type", "Nieznany"),
            address_1=b.get("address_1"),
            city=b.get("city"),
            state_province=b.get("state_province"),
            postal_code=b.get("postal_code"),
            country=b.get("country"),
            longitude=b.get("longitude"),
            latitude=b.get("latitude"),
            phone=b.get("phone"),
            website_url=b.get("website_url"),
        )
        lista_browarow.append(obiekt_brewery)

    # Wyświetlanie informacji, jeśli brak wyników dla danego miasta
    if not lista_browarow:
        print(f"Brak wyników dla miasta: {args.city}")
    else:
        for browar in lista_browarow:
            print(browar)


if __name__ == "__main__":
    main()