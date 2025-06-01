import matplotlib.pyplot as plt
import pandas as pd


def analyze_age_sex_survival(df):
    df_analysis = df.copy()

    df_analysis['AgeGroup'] = pd.cut(df_analysis['Age'],
                                     bins=[0, 12, 18, 35, 60, 100],
                                     labels=['Children (0-12)',
                                             'Teenagers (13-18)',
                                             'Adults (19-35)',
                                             'Middle Aged (36-60)',
                                             'Seniors (60+)'])

    all_age_groups = ['Children (0-12)',
                      'Teenagers (13-18)',
                      'Adults (19-35)',
                      'Middle Aged (36-60)',
                      'Seniors (60+)']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    survived_data = df_analysis[df_analysis['Survived'] == 1]
    died_data = df_analysis[df_analysis['Survived'] == 0]

    survived_male_counts = []
    survived_female_counts = []
    died_male_counts = []
    died_female_counts = []

    for group in all_age_groups:
        male_survived = len(survived_data[
                                (survived_data['AgeGroup'] == group) &
                                (survived_data['Sex'] == 'male')])

        female_survived = len(survived_data[
                                  (survived_data['AgeGroup'] == group) &
                                  (survived_data['Sex'] == 'female')])

        male_died = len(died_data[
                            (died_data['AgeGroup'] == group) &
                            (died_data['Sex'] == 'male')])

        female_died = len(died_data[
                              (died_data['AgeGroup'] == group) &
                              (died_data['Sex'] == 'female')])

        survived_male_counts.append(male_survived)
        survived_female_counts.append(female_survived)

        died_male_counts.append(male_died)
        died_female_counts.append(female_died)

    x_pos = range(len(all_age_groups))
    width = 0.35

    ax1.bar([x - width / 2 for x in x_pos],
            survived_male_counts,
            width,
            label='Male',
            color='blue',
            alpha=0.7)

    ax1.bar([x + width / 2 for x in x_pos],
            survived_female_counts,
            width,
            label='Female',
            color='pink',
            alpha=0.7)

    ax1.set_title('Survived - count', fontsize=16, fontweight='bold')
    graph_produce(all_age_groups,
                  ax1,
                  survived_female_counts,
                  survived_male_counts,
                  width,
                  x_pos)

    ax2.bar([x - width / 2 for x in x_pos],
            died_male_counts,
            width,
            label='Male',
            color='blue',
            alpha=0.7)

    ax2.bar([x + width / 2 for x in x_pos],
            died_female_counts,
            width,
            label='Female',
            color='pink',
            alpha=0.7)

    ax2.set_title('Did not survive - count', fontsize=16, fontweight='bold')
    graph_produce(all_age_groups,
                  ax2,
                  died_female_counts,
                  died_male_counts,
                  width,
                  x_pos)

    plt.tight_layout()
    plt.show()

    return df_analysis


def graph_produce(all_age_groups,
                  ax1,
                  survived_female_counts,
                  survived_male_counts,
                  width,
                  x_pos):
    ax1.set_ylabel('Number of People')
    ax1.set_xlabel('Age Group')

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(all_age_groups, rotation=45)

    ax1.legend()
    for i, (male_val, female_val) in enumerate(zip(survived_male_counts, survived_female_counts)):

        if male_val > 0:
            ax1.text(i - width / 2,
                     male_val + 1,
                     str(male_val),
                     ha='center',
                     fontweight='bold')

        if female_val > 0:
            ax1.text(i + width / 2,
                     female_val + 1,
                     str(female_val),
                     ha='center',
                     fontweight='bold')


def run_survival_analysis(df):
    df_with_groups = analyze_age_sex_survival(df)
    return df_with_groups
