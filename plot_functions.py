import streamlit as st


def get_log_linear_buttons():
    log_linear = {
        "type": "buttons",
        'direction': 'right',
        'showactive': True,
        'x': 0.11,
        'xanchor': "left",
        'y': 1.1,
        'yanchor': "top",
        "buttons": [
            {"label": "linear", "method": "relayout", "args": ["yaxis", {"type": "linear"}]},
            {"label": "log", "method": "relayout", "args": ["yaxis", {"type": "log"}]},
        ]}

    return log_linear


def streamlit_max_width():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
