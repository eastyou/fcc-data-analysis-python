"""Graphing Calculator.

Plots common function families and saves the graphs as PNG files.
Uses matplotlib, which is preinstalled in Google Colab.
"""

import math

import matplotlib.pyplot as plt
import numpy as np


def plot_quadratic(a: float, b: float, c: float, path: str = "quadratic.png") -> str:
    """Plot y = a*x^2 + b*x + c."""
    x = np.linspace(-20, 20, 400)
    y = a * x ** 2 + b * x + c
    plt.figure(figsize=(7, 4.5))
    plt.plot(x, y, label=f"{a}x² + {b}x + {c}")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Quadratic function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def plot_cubic(a: float, b: float, c: float, d: float, path: str = "cubic.png") -> str:
    """Plot y = a*x^3 + b*x^2 + c*x + d."""
    x = np.linspace(-10, 10, 500)
    y = a * x ** 3 + b * x ** 2 + c * x + d
    plt.figure(figsize=(7, 4.5))
    plt.plot(x, y, color="darkorange", label=f"{a}x³ + {b}x² + {c}x + {d}")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Cubic function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def plot_sqrt(a: float, path: str = "sqrt.png") -> str:
    """Plot y = a * sqrt(x)."""
    x = np.linspace(0, 25, 400)
    y = a * np.sqrt(x)
    plt.figure(figsize=(7, 4.5))
    plt.plot(x, y, color="seagreen", label=f"{a}√x")
    plt.title("Square root function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def plot_absolute(a: float, h: float, k: float, path: str = "absolute.png") -> str:
    """Plot y = a * |x - h| + k."""
    x = np.linspace(-20, 20, 500)
    y = a * np.abs(x - h) + k
    plt.figure(figsize=(7, 4.5))
    plt.plot(x, y, color="crimson", label=f"{a}|x - {h}| + {k}")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Absolute value function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def plot_exponential(base: float, path: str = "exponential.png") -> str:
    """Plot y = base^x."""
    x = np.linspace(-10, 10, 400)
    y = base ** x
    plt.figure(figsize=(7, 4.5))
    plt.plot(x, y, color="purple", label=f"{base}^x")
    plt.title("Exponential function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def describe_vertex(a: float, b: float, c: float) -> tuple:
    """Return the vertex of y = a*x^2 + b*x + c."""
    x = -b / (2 * a)
    return round(x, 4), round(a * x ** 2 + b * x + c, 4)


if __name__ == "__main__":
    print("Saved:", plot_quadratic(1, -2, -3))
    print("Saved:", plot_cubic(1, 0, -4, 0))
    print("Saved:", plot_sqrt(2))
    print("Saved:", plot_absolute(1, 2, -1))
    print("Saved:", plot_exponential(2))
    print("Quadratic vertex (1, -2, -3):", describe_vertex(1, -2, -3))
    print("Quadratic roots example:", [round(v, 4) for v in np.roots([1, -2, -3])])
