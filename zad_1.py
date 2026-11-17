"""
Zadanie 1:
Klasa Student z metodą sprawdzającą, czy uczeń zdał (średnia > 50).
"""


class Student:
    def __init__(self, name: str, marks: list):
        self.name = name
        self.marks = marks

    def is_passed(self) -> bool:
        # Zabezpieczenie przed dzieleniem przez zero, jeśli brak ocen
        if not self.marks:
            return False

        # Obliczenie średniej
        srednia = sum(self.marks) / len(self.marks)
        return srednia > 50

    def __str__(self) -> str:
        return f"Student: {self.name}"


if __name__ == "__main__":
    # Obiekt ze średnią > 50 (zda)
    student_zda = Student("Anna Kowalska", [60, 70, 80])

    # Obiekt ze średnią <= 50 (nie zda)
    student_nie_zda = Student("Jan Nowak", [30, 40, 50])

    print(f"{student_zda.name} zdał(a)? {student_zda.is_passed()}")
    print(f"{student_nie_zda.name} zdał(a)? {student_nie_zda.is_passed()}")