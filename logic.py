import re
from typing import Dict


def is_palindrome(text: str) -> bool:
    """Sprawdza, czy ciąg jest palindromem, ignorując wielkość liter i spacje."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def fibonacci(n: int) -> int:
    """Zwraca n-ty element ciągu Fibonacciego."""
    if n < 0:
        raise ValueError("Element ciągu nie może być ujemny.")
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def count_vowels(text: str) -> int:
    """Zlicza liczbę samogłosek w podanym ciągu (uwzględnia polskie znaki)."""
    vowels = set("aeiouyąęó")
    return sum(1 for char in text.lower() if char in vowels)


def calculate_discount(price: float, discount: float) -> float:
    """Zwraca cenę po uwzględnieniu zniżki (0.0 - 1.0)."""
    if not (0 <= discount <= 1):
        raise ValueError("Zniżka musi być w przedziale od 0 do 1.")
    return price * (1 - discount)


def flatten_list(nested_list: list) -> list:
    """Spłaszcza zagnieżdżoną listę."""
    flat = []
    for item in nested_list:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat


def word_frequencies(text: str) -> Dict[str, int]:
    """Zwraca słownik z częstością występowania słów (ignoruje interpunkcję)."""
    words = re.findall(r'\b\w+\b', text.lower())
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def is_prime(n: int) -> bool:
    """Sprawdza, czy liczba jest pierwsza."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True