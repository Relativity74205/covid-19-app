import numpy as np
import pandas as pd


def get_csse_data(value_name: str, min_cases: int, rolling_window: int) -> pd.DataFrame:
    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    path_dict = {'cases': 'time_series_covid19_confirmed_global.csv',
                 'deaths': 'time_series_covid19_deaths_global.csv'
                 }

    df = pd.read_csv(f'{base_url}{path_dict[value_name]}')
    df = df.drop(['Lat', 'Long', 'Province/State'], axis=1)
    df = df.rename(columns={'Country/Region': 'country'})
    df_tidy = tidy_data(df, value_name=value_name, rolling_window=rolling_window)
    df_tidy_filtered = filter_tidy_data(df_tidy=df_tidy, min_cases=min_cases, value_name=value_name)

    return df_tidy_filtered


def tidy_data(df: pd.DataFrame, value_name: str, rolling_window: int) -> pd.DataFrame:
    df_cleaned: pd.DataFrame = (df
                                .groupby('country')[df.columns[1:]]
                                .apply(lambda x: x.sum())
                                .reset_index()
                                )
    df_tidy = df_cleaned.melt(id_vars='country',
                              var_name='date',
                              value_name=value_name)
    df_tidy['date'] = pd.to_datetime(df_tidy['date'])
    df_tidy[f'log_{value_name}'] = calc_log_of_series(df_tidy[value_name])
    df_tidy = calc_increase(df_tidy, rolling_window, value_name)

    return df_tidy


def filter_tidy_data(df_tidy: pd.DataFrame, min_cases: int, value_name: str) -> pd.DataFrame:
    max_date = df_tidy['date'].max()
    min_cases = min_cases
    many_case_countries = df_tidy[(df_tidy['date'] == max_date) & (df_tidy[value_name] > min_cases)]['country'].values
    df_tidy_filtered = df_tidy[df_tidy['country'].isin(many_case_countries)]

    return df_tidy_filtered


def calc_rolling_mean(df: pd.DataFrame, group_by_col: str, rolling_col: str, rolling_window: int) -> pd.DataFrame:
    temp = df.set_index('date').groupby(group_by_col)[rolling_col].rolling(rolling_window).mean()
    df = df.set_index(['country', 'date'])
    df = df.join(temp, rsuffix='_smoothed').reset_index()

    return df


def calc_increase(df: pd.DataFrame, rolling_window: int, value_name: str) -> pd.DataFrame:
    df[f'shifted_{value_name}'] = df.groupby('country')[value_name].shift(periods=1).fillna(0)
    df[f'shifted_log_{value_name}'] = df.groupby('country')[f'log_{value_name}'].shift(periods=1).fillna(0)
    df[f'delta_{value_name}'] = df[value_name] - df[f'shifted_{value_name}']
    df[f'delta_log_{value_name}'] = df[f'log_{value_name}'] - df[f'shifted_log_{value_name}']
    # df['relative_increase'] = df['delta_cases'] / df['cases']
    # df['relative_increase'] = df['relative_increase'].fillna(0)
    # df = calc_rolling_mean(df, 'country', 'relative_increase')
    df = calc_rolling_mean(df, 'country', f'delta_log_{value_name}', rolling_window)
    df[f'factor_{value_name}_increase_smoothed'] = np.exp(df[f'delta_log_{value_name}_smoothed'])

    return df


def calc_log_of_series(s: pd.Series) -> pd.Series:
    log_s = np.log(s)
    log_s[log_s == -np.inf] = 0
    return log_s
