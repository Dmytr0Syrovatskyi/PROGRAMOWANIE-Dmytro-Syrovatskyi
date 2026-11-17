"""
Zadanie 2:
System klas dla biblioteki (Library, Employee, Book, Order)
powiązanych ze sobą relacjami. Wykorzystuje klasę Student z zadania 1.
"""

from zad_1 import Student


class Library:
    def __init__(
        self,
        city: str,
        street: str,
        zip_code: str,
        open_hours: str,
        phone: str,
    ):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self) -> str:
        return (
            f"Biblioteka ({self.city}, ul. {self.street} | "
            f"Otwarte: {self.open_hours})"
        )


class Employee:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        hire_date: str,
        birth_date: str,
        city: str,
        street: str,
        zip_code: str,
        phone: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self) -> str:
        return (
            f"Pracownik: {self.first_name} {self.last_name} "
            f"(Zatrudniony: {self.hire_date})"
        )


class Book:
    def __init__(
        self,
        library: Library,
        publication_date: str,
        author_name: str,
        author_surname: str,
        number_of_pages: int,
    ):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self) -> str:
        return (
            f"Książka: '{self.author_name} {self.author_surname}' "
            f"wyd. {self.publication_date} [{self.library}]"
        )


class Order:
    def __init__(
        self, employee: Employee, student: Student, books: list, order_date: str
    ):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self) -> str:
        # Złączenie wszystkich książek w jeden sformatowany tekst
        books_str = "\n  - ".join([str(b) for b in self.books])

        return (
            f"--- ZAMÓWIENIE z dnia: {self.order_date} ---\n"
            f"Obsługuje: {self.employee}\n"
            f"Wypożycza: {self.student}\n"
            f"Wypożyczone pozycje:\n  - {books_str}\n"
            f"--------------------------------------"
        )


if __name__ == "__main__":
    # 1. Tworzenie 2 bibliotek
    lib1 = Library(
        "Warszawa", "Polna 10", "00-111", "08:00-18:00", "111-222-333"
    )
    lib2 = Library(
        "Kraków", "Długa 5", "30-222", "09:00-17:00", "444-555-666"
    )

    # 2. Tworzenie 3 pracowników
    emp1 = Employee(
        "Jan",
        "Kowalski",
        "2020-01-01",
        "1990-05-10",
        "Warszawa",
        "Krótka 1",
        "00-222",
        "123123123",
    )
    emp2 = Employee(
        "Anna",
        "Nowak",
        "2021-03-15",
        "1992-08-20",
        "Warszawa",
        "Leśna 2",
        "00-333",
        "234234234",
    )
    emp3 = Employee(
        "Piotr",
        "Zalewski",
        "2019-11-20",
        "1985-12-05",
        "Kraków",
        "Wąska 3",
        "30-123",
        "345345345",
    )

    # 3. Tworzenie 3 studentów (wymaga zaimportowanej klasy Student z zad_1)
    stud1 = Student("Marek", [80, 90])
    stud2 = Student("Kasia", [60, 75])
    stud3 = Student("Zosia", [40, 50])

    # 4. Tworzenie 5 książek (z przypisanymi obiektami bibliotek)
    book1 = Book(lib1, "2001", "J.R.R.", "Tolkien", 450)
    book2 = Book(lib1, "1997", "J.K.", "Rowling", 320)
    book3 = Book(lib2, "1925", "F. Scott", "Fitzgerald", 200)
    book4 = Book(lib2, "2010", "Stephen", "King", 600)
    book5 = Book(lib1, "1984", "George", "Orwell", 300)

    # 5. Tworzenie 2 zamówień
    order1 = Order(emp1, stud1, [book1, book2, book5], "2023-10-01")
    order2 = Order(emp3, stud2, [book3, book4], "2023-10-02")

    # 6. Wyświetlanie zamówień
    print(order1)
    print()
    print(order2)