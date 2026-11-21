"""Data Graph Explorer.

Reads a CSV file (or builds sample data) and draws several chart types:
line, bar, scatter, histogram and a moving average comparison.
"""

import csv
import os

import matplotlib.pyplot as plt


def load_csv(path: str) -> dict:
    """Load a CSV with a header row of numeric columns."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    columns: dict = {}
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for key, value in row.items():
                try:
                    columns.setdefault(key, []).append(float(value))
                except (TypeError, ValueError):
                    continue
    return columns


def sample_data() -> dict:
    """Return a small sample dataset."""
    return {
        "month": list(range(1, 13)),
        "sales": [120, 135, 128, 160, 172, 168, 190, 205, 198, 220, 235, 250],
        "costs": [90, 95, 92, 110, 118, 115, 130, 140, 138, 150, 158, 165],
    }


def line_chart(data: dict, x_key: str, y_key: str) -> str:
    """Draw a line chart."""
    plt.figure(figsize=(7, 4))
    plt.plot(data[x_key], data[y_key], marker="o", color="#2563eb")
    plt.title(f"{y_key} over {x_key}")
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.grid(alpha=0.3)
    path = "line-chart.png"
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def bar_chart(data: dict, x_key: str, y_key: str) -> str:
    """Draw a bar chart."""
    plt.figure(figsize=(7, 4))
    plt.bar(data[x_key], data[y_key], color="#f59e0b")
    plt.title(f"{y_key} by {x_key}")
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.grid(axis="y", alpha=0.3)
    path = "bar-chart.png"
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def scatter_chart(data: dict, x_key: str, y_key: str) -> str:
    """Draw a scatter plot."""
    plt.figure(figsize=(7, 4))
    plt.scatter(data[x_key], data[y_key], color="#10b981")
    plt.title(f"{y_key} vs {x_key}")
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.grid(alpha=0.3)
    path = "scatter-chart.png"
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def histogram(data: dict, y_key: str) -> str:
    """Draw a histogram of one column."""
    plt.figure(figsize=(7, 4))
    plt.hist(data[y_key], bins=8, color="#8b5cf6", edgecolor="white")
    plt.title(f"Distribution of {y_key}")
    plt.xlabel(y_key)
    plt.ylabel("frequency")
    path = "histogram.png"
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


def moving_average(values: list, window: int = 3) -> list:
    """Return a simple moving average."""
    result = []
    for index in range(len(values)):
        start = max(0, index - window + 1)
        chunk = values[start:index + 1]
        result.append(sum(chunk) / len(chunk))
    return result


def compare_with_average(data: dict, x_key: str, y_key: str) -> str:
    """Plot the raw series next to its moving average."""
    plt.figure(figsize=(7, 4))
    plt.plot(data[x_key], data[y_key], marker="o", label="raw")
    plt.plot(data[x_key], moving_average(data[y_key]), linestyle="--", label="3-point average")
    plt.title(f"{y_key}: raw vs average")
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.legend()
    plt.grid(alpha=0.3)
    path = "moving-average.png"
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    return path


if __name__ == "__main__":
    dataset = sample_data()
    print("Line:", line_chart(dataset, "month", "sales"))
    print("Bar:", bar_chart(dataset, "month", "sales"))
    print("Scatter:", scatter_chart(dataset, "sales", "costs"))
    print("Histogram:", histogram(dataset, "sales"))
    print("Average:", compare_with_average(dataset, "month", "sales"))
    print("Moving average of sales:", [round(v, 2) for v in moving_average(dataset["sales"])])
