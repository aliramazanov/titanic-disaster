import matplotlib.pyplot as plt
import pandas as pd


def analyze_age_survival(df):
    df_age = df.copy()

    df_age['AgeGroup'] = pd.cut(df_age['Age'],
                                bins=[0, 12, 18, 35, 60, 100],
                                labels=['Children (0-12)',
                                        'Teenagers (13-18)',
                                        'Adults (19-35)',
                                        'Middle Aged (36-60)',
                                        'Seniors (60+)'])

    age_survival = df_age.groupby('AgeGroup', observed=True)['Survived'].mean() * 100

    plt.figure(figsize=(10, 6))
    age_survival.plot(kind='bar', color='skyblue')
    plt.title('Survival Rate by Age Group', fontsize=16)
    plt.ylabel('Survival Rate (%)', fontsize=12)
    plt.xlabel('Age Group', fontsize=12)

    plt.xticks(rotation=45)

    for i, v in enumerate(age_survival):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.show()

    return df_age, age_survival


def run_age_analysis(df):
    df_with_age_groups, age_results = analyze_age_survival(df)
    return df_with_age_groups, age_results
