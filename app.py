import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots

import data_functions as dfunc
import plot_functions as pfunc


def plot(value_name: str, min_cases: int, rolling_window: int):
    df = dfunc.get_csse_data(value_name, min_cases=min_cases, rolling_window=rolling_window)

    fig = make_subplots(rows=1, cols=2)

    subfig1 = px.line(df, x='date', y=value_name, color='country')
    subfig2 = px.line(df, x='date', y=f'factor_{value_name}_increase_smoothed', color='country',
                      hover_data=[value_name])

    amount_countries = len(df.country.unique().tolist())

    for data in subfig1.data:
        fig.add_trace(data, row=1, col=1)
    for data in subfig2.data:
        fig.add_trace(data, row=1, col=2)
    for i in range(amount_countries, 2 * amount_countries):
        fig.data[i].showlegend = False
    fig.update_layout(updatemenus=[pfunc.get_log_linear_buttons()])
    fig.update_layout(width=1440, height=640)
    fig.update_yaxes(title=f'Summed {value_name}', row=1, col=1)
    fig.update_yaxes(title=f'Smoothed daily increase (Rolling {rolling_window} day window)', row=1, col=2)

    return fig


pfunc.streamlit_max_width()
st.sidebar.title("What to do")

metric_input = st.sidebar.selectbox('Select metric', ('cases', 'deaths'))
# y_axis_kind_input = st.sidebar.selectbox('y-axis', ('linear', 'log'))
min_cases_input = st.sidebar.number_input('min_cases', min_value=0, value=1000, format='%d')
rolling_window_input = st.sidebar.number_input('rolling_window', min_value=1, value=3, format='%d')
generated_plot = plot(metric_input, min_cases_input, rolling_window_input)  # , y_axis_kind_input)
st.plotly_chart(generated_plot)
