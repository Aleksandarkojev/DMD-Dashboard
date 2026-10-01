import streamlit as st
import pandas as pd
import altair as alt

# ------------------------------------------------
# INSTÄLLNINGAR
# ------------------------------------------------

st.set_page_config(
    page_title="HR Dashboard",
    layout="wide"
)

# ------------------------------------------------
# FÄRGER
# ------------------------------------------------

HUVUDFARG = "#0B3C5D"
ACCENT = "#D9B310"

# ------------------------------------------------
# CSS
# ------------------------------------------------

st.markdown(f"""
<style>

.block-container {{
    padding-top: 1.5rem;
}}

h1 {{
    color: {HUVUDFARG};
}}

[data-testid="stMetric"] {{
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 5px solid {ACCENT};
    border-radius: 12px;
    padding: 12px;
}}

[data-testid="stMetricLabel"] {{
    color: white;
}}

[data-testid="stMetricValue"] {{
    color: white;
}}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# FUNKTIONER
# ------------------------------------------------

def las(filnamn):
    return pd.read_csv(f"data/{filnamn}")

def stapel(df, x, y, titel):

    st.markdown(f"### {titel}")

    graf = (
        alt.Chart(df)
        .mark_bar(color=HUVUDFARG)
        .encode(
            x=alt.X(x, sort="-y"),
            y=y,
            tooltip=[x, y]
        )
        .properties(height=300)
    )

    st.altair_chart(graf, use_container_width=True)

# -------------------