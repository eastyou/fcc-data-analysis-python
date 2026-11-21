import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    df = pd.read_csv('epa-sea-level.csv')

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], s=10)

    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years_all = pd.Series(range(1880, 2051))
    ax.plot(years_all, res_all.intercept + res_all.slope * years_all, 'r', label='Best fit line')

    recent = df[df['Year'] >= 2000]
    res_recent = linregress(recent['Year'], recent['CSIRO Adjusted Sea Level'])
    years_recent = pd.Series(range(2000, 2051))
    ax.plot(
        years_recent,
        res_recent.intercept + res_recent.slope * years_recent,
        'g',
        label='Best fit line since 2000',
    )

    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')
    ax.legend()

    return fig
