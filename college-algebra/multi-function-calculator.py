"""Multi-Function Calculator.

Solves proportions, linear equations, and converts between
fractions, decimals and percents.
"""

from fractions import Fraction
import math


def solve_proportion(a: float, b: float, c: float) -> float:
    """Solve a / b = c / x for x."""
    if b == 0 or c == 0:
        raise ValueError("b and c must be non-zero")
    return b * c / a if a != 0 else float("inf")


def solve_linear(a: float, b: float, c: float) -> float:
    """Solve a*x + b = c for x."""
    if a == 0:
        raise ValueError("a must be non-zero")
    return (c - b) / a


def fraction_decimal_percent(numerator: int, denominator: int) -> dict:
    """Convert a fraction to decimal and percent."""
    if denominator == 0:
        raise ValueError("denominator must be non-zero")
    value = numerator / denominator
    return {
        "fraction": str(Fraction(numerator, denominator)),
        "decimal": round(value, 6),
        "percent": f"{round(value * 100, 4)}%",
    }


def decimal_to_fraction(value: float) -> str:
    """Convert a decimal to a simplified fraction."""
    return str(Fraction(value).limit_denominator(10000))


def percent_to_decimal(value: float) -> float:
    """Convert a percent to a decimal."""
    return value / 100


def quadratic_roots(a: float, b: float, c: float) -> list:
    """Solve a*x^2 + b*x + c = 0."""
    if a == 0:
        return [solve_linear(b, 0, -c)]
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return []
    root = math.sqrt(discriminant)
    return sorted({round((-b + root) / (2 * a), 6), round((-b - root) / (2 * a), 6)})


def menu() -> None:
    print("Multi-Function Calculator")
    print("1. Solve a proportion (a/b = c/x)")
    print("2. Solve a linear equation (ax + b = c)")
    print("3. Convert fraction to decimal and percent")
    print("4. Convert decimal to a fraction")
    print("5. Convert percent to decimal")
    print("6. Solve a quadratic equation")
    choice = input("Choose 1-6: ").strip()

    if choice == "1":
        a, b, c = (float(input(f"{name}: ")) for name in ("a", "b", "c"))
        print("x =", round(solve_proportion(a, b, c), 6))
    elif choice == "2":
        a, b, c = (float(input(f"{name}: ")) for name in ("a", "b", "c"))
        print("x =", round(solve_linear(a, b, c), 6))
    elif choice == "3":
        numerator = int(input("numerator: "))
        denominator = int(input("denominator: "))
        print(fraction_decimal_percent(numerator, denominator))
    elif choice == "4":
        print(decimal_to_fraction(float(input("decimal: "))))
    elif choice == "5":
        print(percent_to_decimal(float(input("percent: "))))
    elif choice == "6":
        a, b, c = (float(input(f"{name}: ")) for name in ("a", "b", "c"))
        print("roots =", quadratic_roots(a, b, c))
    else:
        print("Unknown choice")


if __name__ == "__main__":
    menu()
