from typing import Dict, Any

import numpy as np
import pandas as pd


np.random.seed(42)
df_org = pd.read_csv('/home/arkadius/dev/corona_app/study/data/Baseline Characteristics and Outcomes of 1591 Patients Infected With SARS-CoV-2 Admitted to ICUs of the Lombardy Region.csv')
size = 1591


def get_age_distribution(df: pd.DataFrame) -> Dict[str, float]:
    df_age = df[(df.Category == 'Age') &
                (df['Category Detailed'] == 'Number')]
    df_age = df_age.drop(['Category', 'Category Detailed', 'All'], axis=1)
    df_age = df_age.astype('int')
    df_age: pd.DataFrame = df_age/df_age.to_numpy().sum()

    return dict(df_age.iloc[0])


def get_gender_distribution(df: pd.DataFrame) -> Dict[str, float]:
    df_count = df[(df['Category'] == 'Gender') & (df['Category Detailed'] == 'Males')]
    df_ref = df[(df['Category'] == 'Age') & (df['Category Detailed'] == 'Number')]
    df_count = df_count.drop(['Category', 'Category Detailed', 'All'], axis=1).astype('int')
    df_ref = df_ref.drop(['Category', 'Category Detailed', 'All'], axis=1).astype('int')
    s_result: pd.DataFrame = df_count.iloc[0]/df_ref.iloc[0]

    return dict(s_result)


def get_comorbidities_distribution(df: pd.DataFrame, comorbidity: str) -> Dict[str, float]:
    df_count = df[(df['Category'] == 'Comorbidities') & (df['Category Detailed'] == comorbidity)]
    df_ref = df[(df['Category'] == 'Comorbidities') & (df['Category Detailed'] == 'Number')]
    df_count = df_count.drop(['Category', 'Category Detailed', 'All'], axis=1).astype('int')
    df_ref = df_ref.drop(['Category', 'Category Detailed', 'All'], axis=1).astype('int')
    s_result: pd.DataFrame = df_count.iloc[0]/df_ref.iloc[0]

    return dict(s_result)


comorbidities = list(df_org[df_org['Category'] == 'Comorbidities']['Category Detailed'])
comorbidities = [ele for ele in comorbidities if ele not in ['Number', 'None']]
d_age = get_age_distribution(df_org)
d_gender = get_gender_distribution(df_org)


def generate_data_age_distributed(age: str, d: Dict, name1: Any, name2: Any) -> Any:
    d = {name1: d[age],
         name2: 1 - d[age]}
    return np.random.choice(list(d.keys()), size=1, p=list(d.values()))[0]


df_patients = pd.DataFrame({
    'number': range(1591),
})
df_patients['age'] = np.random.choice(list(d_age.keys()), size=size, p=list(d_age.values()))
df_patients['gender'] = df_patients.apply(lambda row: generate_data_age_distributed(row.age, d_gender,
                                                                                    'male', 'female'), axis=1)
for comorbidity in comorbidities:
    d_comorbidity = get_comorbidities_distribution(df_org, comorbidity)
    df_patients[comorbidity] = df_patients.apply(lambda row: generate_data_age_distributed(row.age, d_comorbidity,
                                                                                           1, 0), axis=1)
df_patients['comorbidity'] = df_patients[comorbidities].sum(axis=1)


def get_outcome_distribution(df: pd.DataFrame) -> Dict:
    category_ht = 'Outcome patients with hypertension'
    category_nht = 'Outcome patients without hypertension'
    df_ht = df.copy()
    df_ht = df_ht[(df_ht['Category'] == category_ht) & (df_ht['Category Detailed'] != 'Number')]
    df_ht = df_ht.drop(['Category', 'All'], axis=1).set_index('Category Detailed').astype('int')
    df_ht = (df_ht/df_ht.sum(axis=0)).fillna(1/3)
    d_ht = df_ht.to_dict()
    df_nht = df.copy()
    df_nht = df_nht[(df_nht['Category'] == category_nht) & (df_nht['Category Detailed'] != 'Number')]
    df_nht = df_nht.drop(['Category', 'All'], axis=1).set_index('Category Detailed').astype('int')
    df_nht = (df_nht/df_nht.sum(axis=0)).fillna(1/3)
    d_nht = df_nht.to_dict()

    return {0: d_nht, 1: d_ht}


d_outcome = get_outcome_distribution(df_org)


def generate_outcome(age: str, hypertension: bool, d_full: Dict) -> Any:
    d = d_full[hypertension][age]

    return np.random.choice(list(d.keys()), size=1, p=list(d.values()))[0]


df_patients['outcome'] = df_patients.apply(lambda row: generate_outcome(row.age, row.Hypertension, d_outcome), axis=1)
