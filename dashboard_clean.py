import streamlit as st
import pandas as pd
import altair as alt

# ------------------------------------------------
# DESIGN
# ------------------------------------------------

st.set_page_config(
    page_title="HR Dashboard",
    layout="wide"
)

HUVUDFARG = "#0B3C5D"
ACCENT = "#D9B310"
HOJD = 220
BLA = "#4A90D9"
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
# DATA
# ------------------------------------------------

try:
    feedback = pd.read_csv(
        "data/analys HR 3 medelbetyg.csv"
    )


    leverans = pd.read_csv(
        "data/analys_hr_3 leverans.csv"
    )

    trend = pd.read_csv(
        "data/analys HR 4.csv"
    )
    trend = trend.iloc[:-1]

    process = pd.read_csv(
        "data/analys_hr_6_mentorbelastning.csv"
    )

except Exception as e:
    st.error(f"Fel vid inläsning av CSV-filer: {e}")
    st.stop()
# ------------------------------------------------
# KPI
# ------------------------------------------------

totala_uppdrag = int(
    leverans["Antal_Uppdrag"].sum()
)

totala_tidrapporter = int(
    leverans["Antal_Tidrapporter"].sum()
)

bast_feedback = leverans.loc[
    leverans["Medelbetyg_Feedback"].idxmax(),
    "Avdelning"
]

mest_uppdrag = leverans.loc[
    leverans["Antal_Uppdrag"].idxmax(),
    "Avdelning"
]

genomsnittligt_betyg = round(
    leverans["Medelbetyg_Feedback"].mean(),
    1
)

# ------------------------------------------------
# RUBRIK
# ------------------------------------------------

st.title("📊 HR Performance Dashboard")

st.caption(
    "Beslutsstöd för HR- och bemanningsledning"
)

# ------------------------------------------------
# KPI-RAD
# ------------------------------------------------

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Totalt antal uppdrag",
    totala_uppdrag
)

k2.metric(
    "Totalt antal tidrapporter",
    totala_tidrapporter
)

k3.metric(
    "Genomsnittligt kundbetyg",
    genomsnittligt_betyg
)

k4.metric(
    "Bäst feedback",
    bast_feedback
)

k5.metric(
    "Flest uppdrag",
    mest_uppdrag
)

# ------------------------------------------------
# INSIKTER
# ------------------------------------------------

st.caption(
    "🏆 Systemutveckling har flest uppdrag medan Infrastruktur har högst kundbetyg."
)
# ------------------------------------------------
# ------------------------------------------------
# FEEDBACKANALYS
# ------------------------------------------------

st.subheader("⭐ Feedbackanalys")

col1, col2 = st.columns(2)

feedback_chart = (
    alt.Chart(feedback)
    .mark_bar(color=HUVUDFARG)
    .encode(
        x=alt.X("kanal:N", title="Kanal"),
        y=alt.Y("medelbetyg:Q", title="Medelbetyg"),
        tooltip=["kanal", "medelbetyg"]
    )
    .properties(height=HOJD)
)

feedback_volym = (
    alt.Chart(feedback)
    .mark_bar(color=ACCENT)
    .encode(
        y=alt.Y(
            "kanal:N",
            sort="-x",
            title="Kanal"
        ),
        x=alt.X(
            "antal_feedback:Q",
            title="Antal feedback"
        ),
        tooltip=["kanal", "antal_feedback"]
    )
    .properties(height=HOJD)
)

with col1:
    st.altair_chart(
        feedback_chart,
        use_container_width=True
    )

with col2:
    st.altair_chart(
        feedback_volym,
        use_container_width=True
    )


# ------------------------------------------------
# ARBETSBELASTNING
# ------------------------------------------------

st.subheader("📁 Arbetsbelastning")

c1, c2 = st.columns(2)

with c1:

    chart1 = (
        alt.Chart(leverans)
        .mark_bar(color=ACCENT)
        .encode(
            x=alt.X("Antal_Uppdrag:Q", title="Antal uppdrag"),
            y=alt.Y("Avdelning:N", sort="-x", title="Avdelning"),
            tooltip=["Avdelning", "Antal_Uppdrag"]
        )
        .properties(height=HOJD)
    )

    st.altair_chart(chart1, use_container_width=True)

with c2:

    chart2 = (
        alt.Chart(leverans)
        .mark_bar(color=BLA)
        .encode(
            x=alt.X("Avdelning:N", title="Avdelning"),
            y=alt.Y("Antal_Tidrapporter:Q", title="Antal tidrapporter"),
            tooltip=["Avdelning", "Antal_Tidrapporter"]
        )
        .properties(height=HOJD)
    )

    st.altair_chart(chart2, use_container_width=True)


# ------------------------------------------------
# KVALITET OCH UTVECKLING
# ------------------------------------------------

st.subheader("✅ Kvalitet och utveckling")

q1, q2 = st.columns(2)

with q1:

    feedback_avdelning = (
        alt.Chart(leverans)
        .mark_bar(color=BLA)
        .encode(
            x=alt.X("Avdelning:N", title="Avdelning"),
            y=alt.Y("Medelbetyg_Feedback:Q", title="Snittbetyg"),
            tooltip=["Avdelning", "Medelbetyg_Feedback"]
        )
        .properties(height=HOJD, title="Kundbetyg per avdelning")
    )

    st.altair_chart(feedback_avdelning, use_container_width=True)

with q2:

    trend_chart = (
        alt.Chart(trend)
        .mark_line(point=True, color=ACCENT)
        .encode(
            x=alt.X("Manad:O", title="Månad"),
            y=alt.Y("Antal_Tidrapporter:Q", title="Antal tidrapporter"),
            tooltip=["Manad", "Antal_Tidrapporter"]
        )
        .properties(height=HOJD, title="Tidrapporter per månad")
    )

    st.altair_chart(trend_chart, use_container_width=True)

    # ------------------------------------------------
# PROCESSEFFEKTIVITET
# ------------------------------------------------

st.subheader("⚙️ Processeffektivitet")

process_chart = (
    alt.Chart(process)
    .mark_bar(color=BLA)
    .encode(
        x=alt.X("Godkannandemetod:N", title="Godkännandemetod"),
        y=alt.Y("Antal_Tidrapporter:Q", title="Antal tidrapporter"),
        tooltip=["Godkannandemetod", "Antal_Tidrapporter"]
    )
    .properties(height=HOJD)
)

st.altair_chart(process_chart, use_container_width=True)