from typing import Dict, Tuple

import numpy as np
import pandas as pd

import config_odds_ratio


def create_df_from_dict() -> pd.DataFrame:
    d: Dict = config_odds_ratio.analyses_b_estimates
    df = pd.DataFrame(d).transpose()
    df['estimate_lower_ci'] = df['estimate'] - 2 * df['se']
    df['estimate_upper_ci'] = df['estimate'] + 2 * df['se']
    df['odds_ratio'] = np.exp(df['estimate'])
    df['odds_ratio_lower_ci'] = np.exp(df['estimate_lower_ci'])
    df['odds_ratio_upper_ci'] = np.exp(df['estimate_upper_ci'])

    return df


def calc_odds_ratio(age: int, heart: bool, sofa: bool, lymphocyte: int, d_dimer: str, add_intercept: bool)\
        -> Tuple[float, float, float]:
    df: pd.DataFrame = create_df_from_dict()
    if d_dimer == 'bigger 0.5':
        df_dimer_middle = True
        df_dimer_high = False
    elif d_dimer == 'bigger 1.0':
        df_dimer_middle = False
        df_dimer_high = True
    else:
        df_dimer_middle = False
        df_dimer_high = False

    estimate = (df.loc['intercept', 'estimate'] * add_intercept +
                age * df.loc['age', 'estimate'] +
                heart * df.loc['heart', 'estimate'] +
                sofa * df.loc['sofa', 'estimate'] +
                lymphocyte * df.loc['lymphocyte', 'estimate'] +
                df_dimer_middle * df.loc['d_dimer_middle', 'estimate'] +
                df_dimer_high * df.loc['d_dimer_high', 'estimate']
                )

    estimate_lower_ci = (df.loc['intercept', 'estimate_lower_ci'] * add_intercept +
                         age * df.loc['age', 'estimate_lower_ci'] +
                         heart * df.loc['heart', 'estimate_lower_ci'] +
                         sofa * df.loc['sofa', 'estimate_lower_ci'] +
                         lymphocyte * df.loc['lymphocyte', 'estimate_lower_ci'] +
                         df_dimer_middle * df.loc['d_dimer_middle', 'estimate_lower_ci'] +
                         df_dimer_high * df.loc['d_dimer_high', 'estimate_lower_ci']
                         )

    estimate_upper_ci = (df.loc['intercept', 'estimate_upper_ci'] * add_intercept +
                         age * df.loc['age', 'estimate_upper_ci'] +
                         heart * df.loc['heart', 'estimate_upper_ci'] +
                         sofa * df.loc['sofa', 'estimate_upper_ci'] +
                         lymphocyte * df.loc['lymphocyte', 'estimate_upper_ci'] +
                         df_dimer_middle * df.loc['d_dimer_middle', 'estimate_upper_ci'] +
                         df_dimer_high * df.loc['d_dimer_high', 'estimate_upper_ci']
                         )

    return np.exp(estimate), np.exp(estimate_lower_ci), np.exp(estimate_upper_ci)
