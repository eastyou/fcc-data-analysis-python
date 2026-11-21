"""Three Math Games.

1. Scatter Plot Game - guess the coordinates of a hidden point.
2. Algebra Practice Game - solve randomly generated linear equations.
3. Projectile Game - guess the vertex of a parabola.
"""

import random

import matplotlib.pyplot as plt


def scatter_plot_game() -> int:
    """The player guesses a point's coordinates."""
    x, y = random.randint(-10, 10), random.randint(-10, 10)
    score = 0
    for _ in range(3):
        point = (random.randint(-10, 10), random.randint(-10, 10))
        plt.figure(figsize=(4, 4))
        plt.axhline(0, color="black", linewidth=0.8)
        plt.axvline(0, color="black", linewidth=0.8)
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.scatter([point[0]], [point[1]], color="crimson", s=60)
        plt.grid(alpha=0.3)
        plt.title("Where is the point?")
        plt.show()
        guess = (int(input("Guess x: ")), int(input("Guess y: ")))
        if guess == point:
            print("Exact hit!")
            score += 2
        elif abs(guess[0] - point[0]) <= 1 and abs(guess[1] - point[1]) <= 1:
            print("Very close! It was", point)
            score += 1
        else:
            print("Missed. It was", point)
    return score


def algebra_practice_game() -> int:
    """Solve randomly generated equations of the form ax + b = c."""
    score = 0
    for _ in range(5):
        a = random.randint(2, 9)
        x = random.randint(-10, 10)
        b = random.randint(-20, 20)
        c = a * x + b
        answer = int(input(f"Solve {a}x + ({b}) = {c} for x: "))
        if answer == x:
            print("Correct!")
            score += 1
        else:
            print("Not quite. x =", x)
    return score


def projectile_game() -> int:
    """Guess the vertex of y = -x^2 + bx + c."""
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    vertex_x = b / 2
    vertex_y = -(vertex_x ** 2) + b * vertex_x + c
    print(f"Function: y = -x² + {b}x + {c}")
    guess_x = float(input("Guess the x-coordinate of the vertex: "))
    guess_y = float(input("Guess the y-coordinate of the vertex: "))
    if abs(guess_x - vertex_x) < 0.5 and abs(guess_y - vertex_y) < 0.5:
        print("Bullseye!")
        return 1
    print(f"The vertex is ({vertex_x}, {vertex_y})")
    return 0


def menu() -> None:
    total = 0
    print("Three Math Games")
    print("1. Scatter Plot Game")
    print("2. Algebra Practice Game")
    print("3. Projectile Game")
    choice = input("Choose 1-3: ").strip()
    if choice == "1":
        total = scatter_plot_game()
    elif choice == "2":
        total = algebra_practice_game()
    elif choice == "3":
        total = projectile_game()
    else:
        print("Unknown choice")
    print("Score:", total)


if __name__ == "__main__":
    menu()
