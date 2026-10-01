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

BLA = "#4A90D9"       # huvudfärg för alla staplar
ACCENT = "#D9B310"    # används för det som ska sticka ut
HOJD = 280            # samma höjd på alla diagram

st.markdown(f"""
<style>

.block-container {{
    padding-top: 1.5rem;
}}

[data-testid="stMetric"] {{
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 5px solid {ACCENT};
    border-radius: 12px;
    padding: 12px;
}}

[data-testid="stMetricLabel"] {{
    color: #9ca3af;
}}

[data-testid="stMetricValue"] {{
    color: white;
    font-size: 1.6rem;
}}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# DATA
# ------------------------------------------------

try:
    feedback = pd.read_csv("data/analys HR 3 medelbetyg.csv")
    leverans = pd.read_csv("data/analys_hr_3 leverans.csv")
    trend = pd.read_csv("data/analys HR 4.csv")
    process = pd.read_csv("data/analys_hr_6_mentorbelastning.csv")
except Exception as e:
    st.error(f"Fel vid inläsning av CSV-filer: {e}")
    st.stop()

# "null" i CSV-filen läses in som saknat värde, ge det ett tydligt namn
process["Godkannandemetod"] = process["Godkannandemetod"].fillna("Ej angiven")

# ------------------------------------------------
# HJÄLPFUNKTION: ett stapeldiagram med värden på staplarna
# ------------------------------------------------

def stapel(df, kategori, varde, varde_titel, titel, farg=BLA, fmt=".0f"):
    """Liggande staplar, sorterade, med siffran vid varje stapel."""
    maxvarde = float(df[varde].max())

    bas = alt.Chart(df).encode(
        y=alt.Y(f"{kategori}:N", sort="-x", title=None),
        x=alt.X(
            f"{varde}:Q",
            title=varde_titel,
            scale=alt.Scale(domain=[0, maxvarde * 1.15])
        ),
        tooltip=[kategori, varde],
    )

    staplar = bas.mark_bar(color=farg)
    etiketter = bas.mark_text(
        align="left", dx=4, color="white"
    ).encode(text=alt.Text(f"{varde}:Q", format=fmt))

    return (staplar + etiketter).properties(height=HOJD, title=titel)

# ------------------------------------------------
# KPI
# ------------------------------------------------

totala_uppdrag = int(leverans["Antal_Uppdrag"].sum())
totala_tidrapporter = int(leverans["Antal_Tidrapporter"].sum())

bast_feedback = leverans.loc[
    leverans["Medelbetyg_Feedback"].idxmax(), "Avdelning"
]
mest_uppdrag = leverans.loc[
    leverans["Antal_Uppdrag"].idxmax(), "Avdelning"
]
genomsnittligt_betyg = round(leverans["Medelbetyg_Feedback"].mean(), 1)

# ------------------------------------------------
# RUBRIK OCH KPI-RAD
# ------------------------------------------------

st.title("📊 HR Performance Dashboard")
st.caption("Beslutsstöd för HR- och bemanningsledning")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Totalt antal uppdrag", totala_uppdrag)
k2.metric("Totalt antal tidrapporter", totala_tidrapporter)
k3.metric("Genomsnittligt kundbetyg", genomsnittligt_betyg)
k4.metric("Bäst feedback", bast_feedback)
k5.metric("Flest uppdrag", mest_uppdrag)

st.success(
    f"🏆 {mest_uppdrag} har flest uppdrag, medan {bast_feedback} har högst "
    "kundbetyg. Resultatet kan användas som stöd för bemanning och "
    "resursplanering."
)

# ------------------------------------------------
# 1. FEEDBACKANALYS
# ------------------------------------------------

st.subheader("⭐ Feedbackanalys")

f1, f2 = st.columns(2)

with f1:
    st.altair_chart(
        stapel(feedback, "kanal", "medelbetyg",
               "Medelbetyg", "Medelbetyg per kanal", fmt=".1f"),
        use_container_width=True
    )

with f2:
    st.altair_chart(
        stapel(feedback, "kanal", "antal_feedback",
               "Antal feedback", "Antal feedback per kanal", farg=ACCENT),
        use_container_width=True
    )

# ------------------------------------------------
# 2. AVDELNINGAR
# ------------------------------------------------

st.subheader("🏢 Avdelningar")

a1, a2, a3 = st.columns(3)

with a1:
    st.altair_chart(
        stapel(leverans, "Avdelning", "Antal_Uppdrag",
               "Antal uppdrag", "Uppdrag per avdelning"),
        use_container_width=True
    )

with a2:
    st.altair_chart(
        stapel(leverans, "Avdelning", "Antal_Tidrapporter",
               "Antal tidrapporter", "Tidrapporter per avdelning"),
        use_container_width=True
    )

with a3:
    st.altair_chart(
        stapel(leverans, "Avdelning", "Medelbetyg_Feedback",
               "Snittbetyg", "Kundbetyg per avdelning", fmt=".1f"),
        use_container_width=True
    )

# ------------------------------------------------
# 3. TID OCH PROCESS
# ------------------------------------------------

st.subheader("📈 Tid och process")

t1, t2 = st.columns(2)

with t1:
    trend_chart = (
        alt.Chart(trend)
        .mark_line(point=True, color=ACCENT)
        .encode(
            x=alt.X("Manad:O", title="Månad",
                    axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Antal_Tidrapporter:Q", title="Antal tidrapporter",
                    scale=alt.Scale(zero=True)),
            tooltip=["Manad", "Antal_Tidrapporter"]
        )
        .properties(height=HOJD, title="Tidrapporter per månad")
    )
    st.altair_chart(trend_chart, use_container_width=True)

with t2:
    st.altair_chart(
        stapel(process, "Godkannandemetod", "Antal_Tidrapporter",
               "Antal tidrapporter", "Tidrapporter per godkännandemetod"),
        use_container_width=True
    )
