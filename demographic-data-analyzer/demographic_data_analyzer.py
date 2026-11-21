import pandas as pd


def calculate_demographic_data(print_data=True):
    df = pd.read_csv('adult.data.csv')

    race_count = df['race'].value_counts()

    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    total = len(df)
    bachelors = len(df[df['education'] == 'Bachelors'])
    percentage_bachelors = round(bachelors / total * 100, 1)

    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    higher_education_rich = round(
        len(df[higher_education & (df['salary'] == '>50K')]) / len(df[higher_education]) * 100, 1
    )
    lower_education_rich = round(
        len(df[lower_education & (df['salary'] == '>50K')]) / len(df[lower_education]) * 100, 1
    )

    min_work_hours = df['hours-per-week'].min()
    min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round(len(min_workers[min_workers['salary'] == '>50K']) / len(min_workers) * 100, 1)

    countries = df['native-country'].value_counts()
    rich_countries = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_ratio = (rich_countries / countries * 100).sort_values(ascending=False)
    highest_earning_country = country_ratio.index[0]
    highest_earning_country_percentage = round(country_ratio.iloc[0], 1)

    top_in = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].value_counts()
    top_IN_occupation = top_in.index[0]

    if print_data:
        print('Number of each race:\n', race_count)
        print('Average age of men:', average_age_men)
        print('Percentage with Bachelors degrees:', percentage_bachelors, '%')
        print('Percentage with higher education that earn >50K:', higher_education_rich, '%')
        print('Percentage without higher education that earn >50K:', lower_education_rich, '%')
        print('Min work time:', min_work_hours, 'hours/week')
        print('Percentage of rich among those who work fewest hours:', rich_percentage, '%')
        print('Country with highest percentage of rich:', highest_earning_country)
        print('Highest percentage of rich people in country:', highest_earning_country_percentage, '%')
        print('Top occupations in India:', top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation,
    }
