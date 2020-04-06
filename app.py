import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots

import data_functions as dfunc
import plot_functions as pfunc
import odds_ratio_functions as orf


def plot(df: pd.DataFrame, base_metric: str, flag_delta: bool, rolling_window: int):
    fig = make_subplots(rows=1, cols=2)

    if flag_delta:
        subfig1 = px.line(df, x='date', y=f'delta_{base_metric}', color='country')
    else:
        subfig1 = px.line(df, x='date', y=base_metric, color='country')

    subfig2 = px.line(df, x='date', y=f'factor_{base_metric}_increase_smoothed', color='country',
                      hover_data=[base_metric, f'delta_{base_metric}'])

    amount_countries = len(df.country.unique().tolist())

    for data in subfig1.data:
        fig.add_trace(data, row=1, col=1)
    for data in subfig2.data:
        fig.add_trace(data, row=1, col=2)
    for i in range(amount_countries, 2 * amount_countries):
        fig.data[i].showlegend = False
    fig.update_layout(updatemenus=[pfunc.get_log_linear_buttons()])
    fig.update_layout(width=1440, height=640)
    if flag_delta:
        fig.update_yaxes(title=f'Daily delta of {base_metric}', row=1, col=1)
    else:
        fig.update_yaxes(title=f'Cummulated sum of {base_metric}', row=1, col=1)
    fig.update_yaxes(title=f'Smoothed daily increase (Rolling {rolling_window} day window)', row=1, col=2)

    return fig


def get_data(value_name: str, min_cases: int, rolling_window: int):
    df = dfunc.get_csse_data(value_name, min_cases=min_cases, rolling_window=rolling_window)

    return df


def main_statistics():
    st.sidebar.title("What to do")
    metric_input = st.sidebar.selectbox('Select metric', ('cases', 'delta_cases', 'deaths', 'delta_deaths'))
    min_cases_input = st.sidebar.number_input('min_cases', min_value=0, value=1000, format='%d')
    rolling_window_input = st.sidebar.number_input('rolling_window', min_value=1, value=3, format='%d')

    if 'cases' in metric_input:
        base_metric = 'cases'
    else:
        base_metric = 'deaths'

    df = get_data(base_metric, min_cases_input, rolling_window_input)
    if 'delta' in metric_input:
        generated_plot = plot(df, base_metric, True, rolling_window_input)
    else:
        generated_plot = plot(df, base_metric, False, rolling_window_input)

    st.plotly_chart(generated_plot)


def main_odds_ratios():
    st.sidebar.header('Choose parameters')
    age: int = st.sidebar.number_input('Age', min_value=0, value=20)
    heart: bool = st.sidebar.checkbox('Coronary heart diseases')
    sofa: bool = st.sidebar.checkbox('SOFA score')
    lymphocyte: int = st.sidebar.number_input('Lymphocyte count (× 10 9 /L)', min_value=0, value=0)
    d_dimer: str = st.sidebar.selectbox('D-dimer (microgramm/L)', ('smaller 0.5', 'bigger 0.5', 'bigger 1.0'))
    odds_ratio, odds_ratio_lower_ci, odds_ratio_upper_ci = orf.calc_odds_ratio(age, heart, sofa, lymphocyte, d_dimer)

    st.write(f'Estimated odds_ratio for the settings is {odds_ratio:.2f}, '
             f'CI ({odds_ratio_lower_ci:.2f}-{odds_ratio_upper_ci:.2f}).')


def main():
    mode: str = st.sidebar.selectbox('App mode', ('Numbers', 'Odds'))
    pfunc.streamlit_max_width()
    if mode == 'Numbers':
        main_statistics()
    else:
        main_odds_ratios()


if __name__ == '__main__':
    main()
