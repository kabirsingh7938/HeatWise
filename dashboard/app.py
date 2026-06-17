import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="HeatWise",
    page_icon="🔥",
    layout="wide"
)

# ==================================
# LOAD DISTRICT DATA
# ==================================

df = pd.read_csv("../data/HeatWise_Delhi_District_Intelligence.csv")

df.columns = df.columns.str.strip()

# ==================================
# METRICS
# ==================================

avg_temp = df["Avg_LST"].mean()
avg_ndvi = df["Avg_NDVI"].mean()
avg_ndbi = df["Avg_NDBI"].mean()

hottest = df.loc[df["Avg_LST"].idxmax()]
coolest = df.loc[df["Avg_LST"].idxmin()]
greenest = df.loc[df["Avg_NDVI"].idxmax()]
builtup = df.loc[df["Avg_NDBI"].idxmax()]

# ==================================
# HEATWISE SCORE
# ==================================

score = 100
score -= (avg_temp - 35) * 2
score += avg_ndvi * 25
score -= avg_ndbi * 20

score = max(0, min(100, int(score)))

if score < 40:
    risk = "🔴 HIGH RISK"
elif score < 70:
    risk = "🟡 MODERATE RISK"
else:
    risk = "🟢 LOW RISK"

# ==================================
# HEADER
# ==================================

st.title("🔥 HeatWise")

st.subheader(
    "AI-Powered Urban Heat Intelligence Platform"
)

st.markdown("""
HeatWise combines satellite imagery,
remote sensing, and machine learning
to identify urban heat risks and
recommend cooling interventions.
""")

# ==================================
# MAIN METRICS
# ==================================

st.write("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌡 Avg Temperature",
        f"{avg_temp:.2f} °C"
    )

with col2:
    st.metric(
        "🌿 Avg NDVI",
        f"{avg_ndvi:.2f}"
    )

with col3:
    st.metric(
        "🏢 Avg NDBI",
        f"{avg_ndbi:.2f}"
    )

with col4:
    st.metric(
        "🔥 HeatWise Score",
        f"{score}/100"
    )

# ==================================
# RISK ASSESSMENT
# ==================================

st.write("---")

st.header("🤖 AI Heat Risk Assessment")

if score < 40:
    st.error(risk)
elif score < 70:
    st.warning(risk)
else:
    st.success(risk)

# ==================================
# DISTRICT INSIGHTS
# ==================================

st.write("---")

st.header("🏙 District Intelligence")

a, b = st.columns(2)

with a:
    st.error(
        f"🔥 Hottest District: {hottest['DISTRICT']} ({hottest['Avg_LST']:.2f} °C)"
    )

with b:
    st.success(
        f"🌡 Coolest District: {coolest['DISTRICT']} ({coolest['Avg_LST']:.2f} °C)"
    )

c, d = st.columns(2)

with c:
    st.success(
        f"🌿 Greenest District: {greenest['DISTRICT']} (NDVI {greenest['Avg_NDVI']:.3f})"
    )

with d:
    st.warning(
        f"🏢 Most Built-Up District: {builtup['DISTRICT']} (NDBI {builtup['Avg_NDBI']:.3f})"
    )

# ==================================
# PLATFORM MODULES
# ==================================

st.write("---")

st.header("🚀 Explore HeatWise")

st.markdown("""
🏠 **Overview**

🗺 **Heat Map**

🤖 **AI Advisor**

🔮 **Forecast**

🌳 **Cooling Simulator**

📊 **Analytics**
""")

st.write("---")

st.header("🏆 Hottest Districts")

top3 = df.sort_values(
    "Avg_LST",
    ascending=False
).head(3)

for i, row in enumerate(top3.itertuples(), start=1):

    medal = ["🥇", "🥈", "🥉"][i-1]

    st.warning(
        f"{medal} {row.DISTRICT} — {row.Avg_LST:.2f} °C"
    )
    
# ==================================
# EXECUTIVE SUMMARY
# ==================================

st.write("---")

st.header("🌍 Executive Summary")

st.info(f"""
Delhi Average Temperature: {avg_temp:.2f} °C

🔥 Hottest District: {hottest['DISTRICT']}

🌡 Coolest District: {coolest['DISTRICT']}

🌿 Greenest District: {greenest['DISTRICT']}

🏢 Most Built-Up District: {builtup['DISTRICT']}

HeatWise now uses district-level satellite intelligence
instead of anonymous sample points.
""")

# ==================================
# STATUS
# ==================================

st.write("---")

st.success(
    """
✅ HeatWise District Intelligence System Active

Data Source:
Google Earth Engine

Satellite Products:
• Landsat 8 Surface Temperature
• Sentinel-2 Vegetation Analysis

Analysis Period:
May–June 2024
"""
)