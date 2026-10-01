import streamlit as st
import pandas as pd
import altair as alt

# ------------------
# DASHBOARD DESIGN
# ------------------

st.set_page_config(
    page_title="HR Dashboard",
    layout="wide"
)

HUVUDFARG = "#0B3C5D"
ACCENT = "#D9B310"

st.markdown(f"""
<style>
.block-container {{
    padding-top: 1.5rem;
}}

h1 {{
    color: {HUVUDFARG};
}}

[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 5px solid #D9B310;
    border-radius: 10px;
    padding: 12px;
}

[data-testid="stMetricLabel"] {
    color: white;
}

[data-testid="stMetricValue"] {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------
# FUNKTIONER
# ------------------

def las(filnamn):
    try:
        return pd.read_csv(f"data/{filnamn}")
    except FileNotFoundError:
        st.error(f"Hittar inte filen: data/{filnamn}")
        return pd.DataFrame()

def summa(df, kolumn):
    if kolumn in df.columns:
        return df[kolumn].sum()
    return 0

def tal(varde):
    return f"{varde:,.0f}".replace(",", " ")

HOJD = 130

def stapel(df, x, y, titel):

    with st.container(border=True):

        st.markdown(f"**{titel}**")

        if df.empty:
            return

        graf = (
            alt.Chart(df)
            .mark_bar(
                color=HUVUDFARG,
                cornerRadiusTopLeft=4,
                cornerRadiusTopRight=4
            )
            .encode(
                x=alt.X(
                    x,
                    sort="-y",
                    title=None,
                    axis=alt.Axis(labelAngle=0)
                ),
                y=alt.Y(y, title=None),
                tooltip=[x, y]
            )
            .properties(height=HOJD)
        )

        st.altair_chart(
            graf,
            width="stretch"
        )

def liggande(df, x, y, titel):

    with st.container(border=True):

        st.markdown(f"**{titel}**")

        if df.empty:
            return

        graf = (
            alt.Chart(df)
            .mark_bar(
                color=ACCENT,
                cornerRadiusTopRight=4,
                cornerRadiusBottomRight=4
            )
            .encode(
                y=alt.Y(
                    x,
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    y,
                    title=None
                ),
                tooltip=[x, y]
            )
            .properties(height=HOJD)
        )

        st.altair_chart(
            graf,
            width="stretch"
        )

# ------------------------------------------------
# DATA
# ------------------------------------------------

klass = las("analys HR 3 medelbetyg.csv")
leverans = las("analys_hr_3 leverans.csv")
trend = las("analys HR 4.csv")
godkannande = las("analys_hr_6_mentorbelastning.csv")

# Sortera
if not leverans.empty:

    leverans = leverans.sort_values(
        by="Antal_Uppdrag",
        ascending=False
    )

# ------------------------------------------------
# RUBRIK
# ------------------------------------------------

st.title("📊 HR Performance Dashboard")

st.caption(
    "Beslutsstöd för HR- och bemanningsledning"
)

# ------------------------------------------------
# KPI
# ------------------------------------------------

uppdrag = summa(
    leverans,
    "Antal_Uppdrag"
)

tidrapporter = summa(
    leverans,
    "Antal_Tidrapporter"
)

if not leverans.empty:

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

else:

    bast_feedback = "-"
    mest_uppdrag = "-"
    genomsnittligt_betyg = "-"

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Totalt antal uppdrag",
    tal(uppdrag)
)

k2.metric(
    "Totalt antal tidrapporter",
    tal(tidrapporter)
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

st.info("""
Analysen visar att Systemutveckling och Dataanalys står för den största delen av verksamhetens uppdrag och tidrapportering. Infrastruktur har färre uppdrag men det högsta genomsnittliga kundbetyget.
""")

# ------------------------------------------------
# FEEDBACKANALYS
# ------------------------------------------------

st.subheader("⭐ Feedbackanalys")

v, h = st.columns(2)

with v:
    stapel(
        klass,
        x="kanal",
        y="medelbetyg",
        titel="Medelbetyg per kanal"
    )

with h:
    liggande(
        klass,
        x="kanal",
        y="medelbetyg",
        titel="Ranking av kanaler efter feedback"
    )

# ------------------------------------------------
# ARBETSBELASTNING
# ------------------------------------------------

st.subheader("📁 Arbetsbelastning")

v, h = st.columns(2)

with v:

    liggande(
        leverans,
        x="Avdelning",
        y="Antal_Uppdrag",
        titel="Vilken avdelning har flest uppdrag?"
    )

with h:

    stapel(
        leverans,
        x="Avdelning",
        y="Antal_Tidrapporter",
        titel="Vilken avdelning har flest tidrapporter?"
    )

st.success(
    f"🏆 {mest_uppdrag} har flest uppdrag i organisationen."
)

# ------------------------------------------------
# AVDELNINGSKVALITET
# ------------------------------------------------

st.subheader("✅ Avdelningskvalitet")

v, h = st.columns(2)

with v:

    liggande(
        leverans,
        x="Avdelning",
        y="Medelbetyg_Feedback",
        titel="Vilken avdelning får bäst feedback?"
    )

with h:

    stapel(
        leverans,
        x="Avdelning",
        y="Medelbetyg_Feedback",
        titel="Feedback per avdelning"
    )

st.success(
    f"⭐ {bast_feedback} har högst kundbetyg."
)

# ------------------------------------------------
# TREND
# ------------------------------------------------

st.subheader("📈 Utveckling över tid")

stapel(
    trend,
    x="Manad",
    y="Antal_Tidrapporter",
    titel="Tidrapportering per månad"
)

# ------------------------------------------------
# PROCESSEFFEKTIVITET
# ------------------------------------------------

st.subheader("⚙️ Processeffektivitet")

stapel(
    godkannande,
    x="Godkannandemetod",
    y="Antal_Tidrapporter",
    titel="Hur godkänns tidrapporter?"
)