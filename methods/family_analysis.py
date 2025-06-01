import matplotlib.pyplot as plt


def create_family_analysis(df):
    df_family = df.copy()

    df_family['Surname'] = df_family['Name'].str.split(',').str[0].str.strip()
    df_family['FamilyID'] = df_family['Ticket']

    for surname in df_family['Surname'].unique():
        people_with_surname = df_family[df_family['Surname'] == surname]

        if len(people_with_surname) > 1:
            family_claims = (people_with_surname['SibSp'] +
                             people_with_surname['Parch'])

            if family_claims.sum() > 0:
                for (passenger_class, port), group in (
                        people_with_surname.groupby(['Pclass', 'Embarked'])):

                    if len(group) > 1:
                        family_id = f"{surname}_{passenger_class}_{port}"
                        df_family.loc[group.index, 'FamilyID'] = family_id

    family_sizes = df_family.groupby('FamilyID').size()

    df_family['FamilySize'] = df_family['FamilyID'].map(family_sizes)
    df_family['SimpleFamilySize'] = df_family['SibSp'] + df_family['Parch'] + 1

    def get_category(size):
        if size == 1:
            return 'Alone'
        elif size == 2:
            return 'Couple'
        elif size in [3, 4]:
            return 'Small Family'
        elif size in [5, 6]:
            return 'Medium Family'
        elif size in [7, 8, 9]:
            return 'Large Family'
        elif size in [10, 11, 12]:
            return 'Extra Large Family'
        else:
            return 'Outlier Family'

    df_family['Category'] = df_family['FamilySize'].apply(get_category)

    return df_family


def check_family_identification(df_family):
    all_families = df_family.groupby('FamilyID').size()

    print(f"Found {len(all_families)} families")

    print(f"Biggest family: {all_families.max()} people")

    print(f"People traveling alone: {sum(all_families == 1)}")
    print(f"People in groups: {sum(all_families > 1)}")

    problems = df_family[abs(df_family['FamilySize']
                             - df_family['SimpleFamilySize']) > 2]

    print(f"Potential problems: {len(problems)} cases")

    known_families = ['Sage', 'Andersson', 'Rice', 'Goodwin', 'Panula']

    print("\nKnown large families:")

    for surname in known_families:
        matches = df_family[df_family['Surname'] == surname]

        if len(matches) > 0:
            groups = matches.groupby('FamilyID').size()
            print(f"  {surname}: {len(matches)} people in {len(groups)} groups")

    claim_family = df_family[(df_family['SibSp'] > 0) | (df_family['Parch'] > 0)]

    alone_but_claim = claim_family[claim_family['FamilySize'] == 1]
    print(f"\nPeople claiming family but alone: {len(alone_but_claim)}")

    issues = len(problems) + len(alone_but_claim)
    accuracy = ((len(df_family) - issues) / len(df_family) * 100)

    print(f"Estimated accuracy: {accuracy:.1f}%")


def calculate_survival_rates(df_family):
    results = df_family.groupby('Category')['Survived'].agg(['count', 'sum', 'mean']).round(3)
    results.columns = ['Total', 'Survived', 'SurvivalRate']
    results['Percentage'] = (results['SurvivalRate'] * 100).round(1)

    return results


def show_results(results):
    print("\nSurvival Results:")

    for category, row in results.iterrows():
        print(f"{category}: {row['Survived']:.0f}/{row['Total']:.0f} "
              f"people survived ({row['Percentage']:.1f}%)")


def create_charts(df_family, results):
    fig, (chart1, chart2) = plt.subplots(1, 2, figsize=(12, 5))

    df_family['Category'].value_counts().plot(kind='bar', ax=chart1)
    chart1.set_title('How Many People in Each Family Size')
    chart1.set_ylabel('Number of People')

    results['Percentage'].plot(kind='bar', ax=chart2)
    chart2.set_title('Survival Rate by Family Size')
    chart2.set_ylabel('Survival Rate (%)')

    plt.tight_layout()
    plt.show()


def run_family_analysis(df):
    df_with_families = create_family_analysis(df)
    check_family_identification(df_with_families)
    survival_results = calculate_survival_rates(df_with_families)
    show_results(survival_results)
    create_charts(df_with_families, survival_results)

    return df_with_families, survival_results
