import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Overview",
    page_icon="🏠",
    layout="wide"
)

# ==================================
# LOAD DISTRICT DATA
# ==================================

csv_file = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "HeatWise_Delhi_District_Intelligence.csv"
)

df = pd.read_csv(csv_file)

# ==================================
# CLEAN COLUMN NAMES
# ==================================

df.columns = df.columns.str.strip()

# ==================================
# KEY INSIGHTS
# ==================================

hottest = df.loc[df["Avg_LST"].idxmax()]
coolest = df.loc[df["Avg_LST"].idxmin()]
greenest = df.loc[df["Avg_NDVI"].idxmax()]
builtup = df.loc[df["Avg_NDBI"].idxmax()]

avg_temp = df["Avg_LST"].mean()
avg_ndvi = df["Avg_NDVI"].mean()
avg_ndbi = df["Avg_NDBI"].mean()

resilience_score = int(
    100
    - (avg_temp - 40) * 2
    + avg_ndvi * 50
    - avg_ndbi * 20
)

resilience_score = max(
    0,
    min(100, resilience_score)
)

# ==================================
# HEADER
# ==================================

st.title("🏠 HeatWise Overview")

st.markdown("""
AI-powered Urban Heat Intelligence Platform
for understanding temperature, vegetation,
and built-up impacts across Delhi districts.
""")

# ==================================
# METRICS
# ==================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "🌡 Avg Temperature",
        f"{avg_temp:.2f} °C"
    )

with c2:
    st.metric(
        "🌿 Avg NDVI",
        f"{avg_ndvi:.2f}"
    )

with c3:
    st.metric(
        "🏢 Avg NDBI",
        f"{avg_ndbi:.2f}"
    )

with c4:
    st.metric(
        "🔥 Urban Heat Resilience Score",
        f"{resilience_score}/100"
    )

st.write("---")

# ==================================
# HEAT RISK
# ==================================

st.subheader("🤖 AI Heat Risk Assessment")

if avg_temp > 48:
    st.error("🔴 HIGH HEAT RISK")
elif avg_temp > 45:
    st.warning("🟠 MODERATE HEAT RISK")
else:
    st.success("🟢 LOW HEAT RISK")

st.write("---")

# ==================================
# DISTRICT INSIGHTS
# ==================================

st.subheader("🏙 District Intelligence")

a, b = st.columns(2)

with a:
    st.error(
        f"""
### 🔥 Hottest District

**{hottest['DISTRICT']}**

Temperature:
**{hottest['Avg_LST']:.2f} °C**
"""
    )

with b:
    st.success(
        f"""
### 🌡 Coolest District

**{coolest['DISTRICT']}**

Temperature:
**{coolest['Avg_LST']:.2f} °C**
"""
    )

c, d = st.columns(2)

with c:
    st.success(
        f"""
### 🌿 Greenest District

**{greenest['DISTRICT']}**

NDVI:
**{greenest['Avg_NDVI']:.3f}**
"""
    )

with d:
    st.warning(
        f"""
### 🏢 Most Built-Up District

**{builtup['DISTRICT']}**

NDBI:
**{builtup['Avg_NDBI']:.3f}**
"""
    )

st.write("---")

# ==================================
# TOP 3 HOTTEST DISTRICTS
# ==================================

st.subheader("🏆 Heat Hotspot Leaderboard")

top3 = df.sort_values(
    "Avg_LST",
    ascending=False
).head(3)

medals = ["🥇", "🥈", "🥉"]

for i, row in enumerate(
    top3.itertuples(),
    start=0
):
    st.warning(
        f"{medals[i]} {row.DISTRICT} — {row.Avg_LST:.2f} °C"
    )

st.write("---")

# ==================================
# DISTRICT RANKINGS
# ==================================

st.subheader("📊 District Rankings")

ranking = df.sort_values(
    "Avg_LST",
    ascending=False
)[
    [
        "DISTRICT",
        "Avg_LST",
        "Avg_NDVI",
        "Avg_NDBI"
    ]
].copy()

ranking.columns = [
    "District",
    "Temperature (°C)",
    "Vegetation Index",
    "Built-up Index"
]

st.dataframe(
    ranking,
    use_container_width=True
)

st.write("---")

# ==================================
# METHODOLOGY
# ==================================

st.subheader("🔬 Methodology")

st.markdown("""
### HeatWise Processing Pipeline

🛰 Landsat 8 Collection 2  
→ Land Surface Temperature (LST)

🛰 Sentinel-2 Harmonized  
→ NDVI (Vegetation Index)

🛰 Sentinel-2 Harmonized  
→ NDBI (Built-up Index)

⚙ Google Earth Engine  
→ Satellite Data Processing

🏙 District Aggregation  
→ Delhi District Intelligence Dataset

🤖 HeatWise Analytics Engine  
→ Risk Assessment, Forecasting,
Cooling Simulation and Reporting
""")

st.write("---")

# ==================================
# SUMMARY
# ==================================

st.subheader("🌍 Executive Summary")

st.info(
    f"""
Delhi Average Temperature:
{avg_temp:.2f} °C

🔥 Hottest District:
{hottest['DISTRICT']}

🌡 Coolest District:
{coolest['DISTRICT']}

🌿 Greenest District:
{greenest['DISTRICT']}

🏢 Most Built-Up District:
{builtup['DISTRICT']}

HeatWise uses district-level satellite intelligence
derived from remote sensing datasets to support
urban heat assessment and climate-resilient planning.
"""
)

st.write("---")

# ==================================
# DATA SOURCES
# ==================================

st.success("""
✅ HeatWise District Intelligence System

Data Sources:
• Google Earth Engine
• Landsat 8 Collection 2
• Sentinel-2 Harmonized

Study Area:
Delhi, India

Analysis Period:
May–June 2024
""")
