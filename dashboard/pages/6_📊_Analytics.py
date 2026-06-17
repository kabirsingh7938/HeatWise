import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================

csv_file = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "HeatWise_Delhi_District_Intelligence.csv"
)

df = pd.read_csv(csv_file)
df.columns = df.columns.str.strip()

# ==================================
# PAGE HEADER
# ==================================

st.title("📊 HeatWise District Analytics")

st.markdown("""
Advanced district-level urban heat intelligence
for Delhi using satellite imagery and AI analysis.
""")

# ==================================
# METRICS
# ==================================

avg_temp = df["Avg_LST"].mean()

hottest = df.loc[df["Avg_LST"].idxmax()]
coolest = df.loc[df["Avg_LST"].idxmin()]
greenest = df.loc[df["Avg_NDVI"].idxmax()]
builtup = df.loc[df["Avg_NDBI"].idxmax()]

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "🌡 Average Temperature",
        f"{avg_temp:.2f} °C"
    )

with c2:
    st.metric(
        "🔥 Hottest District",
        hottest["DISTRICT"]
    )

with c3:
    st.metric(
        "❄️ Coolest District",
        coolest["DISTRICT"]
    )

# ==================================
# DISTRICT INTELLIGENCE SUMMARY
# ==================================

st.write("---")

st.header("🏙 District Intelligence Summary")

a, b = st.columns(2)

with a:
    st.error(
        f"🔥 Hottest District: {hottest['DISTRICT']} ({hottest['Avg_LST']:.2f} °C)"
    )

with b:
    st.success(
        f"❄️ Coolest District: {coolest['DISTRICT']} ({coolest['Avg_LST']:.2f} °C)"
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
# HEAT RANKINGS
# ==================================

st.write("---")

st.header("🔥 District Heat Rankings")

heat_rankings = df.sort_values(
    "Avg_LST",
    ascending=False
)

display_df = heat_rankings[
    [
        "DISTRICT",
        "Avg_LST",
        "Avg_NDVI",
        "Avg_NDBI"
    ]
].copy()

def classify_risk(temp):
    if temp >= 48:
        return "🔴 High"
    elif temp >= 45:
        return "🟠 Moderate"
    else:
        return "🟢 Low"

display_df["Risk"] = display_df[
    "Avg_LST"
].apply(classify_risk)

display_df.columns = [
    "District",
    "Temperature (°C)",
    "Vegetation Index",
    "Built-up Index",
    "Heat Risk"
]

st.dataframe(
    display_df,
    use_container_width=True
)

# ==================================
# HOTTEST DISTRICTS
# ==================================

st.write("---")

st.header("🔥 Hottest Districts")

st.bar_chart(
    heat_rankings.set_index(
        "DISTRICT"
    )["Avg_LST"]
)

# ==================================
# GREENEST DISTRICTS
# ==================================

st.write("---")

st.header("🌿 Vegetation Analysis")

green_rankings = df.sort_values(
    "Avg_NDVI",
    ascending=False
)

st.bar_chart(
    green_rankings.set_index(
        "DISTRICT"
    )["Avg_NDVI"]
)

# ==================================
# BUILT-UP ANALYSIS
# ==================================

st.write("---")

st.header("🏢 Built-Up Intensity Analysis")

built_rankings = df.sort_values(
    "Avg_NDBI",
    ascending=False
)

st.bar_chart(
    built_rankings.set_index(
        "DISTRICT"
    )["Avg_NDBI"]
)

# ==================================
# TEMPERATURE VS VEGETATION
# ==================================

st.write("---")

st.header("🌿 Temperature vs Vegetation")

scatter_df = df.rename(
    columns={
        "Avg_LST": "Temperature",
        "Avg_NDVI": "Vegetation"
    }
)

st.scatter_chart(
    scatter_df,
    x="Vegetation",
    y="Temperature"
)

# ==================================
# AI INSIGHTS
# ==================================

st.write("---")

st.header("🧠 AI Insights")

st.info(f"""
🔥 Hottest District:
{hottest['DISTRICT']}
({hottest['Avg_LST']:.2f} °C)

❄️ Coolest District:
{coolest['DISTRICT']}
({coolest['Avg_LST']:.2f} °C)

🌿 Greenest District:
{greenest['DISTRICT']}
(NDVI {greenest['Avg_NDVI']:.3f})

🏢 Most Built-Up District:
{builtup['DISTRICT']}
(NDBI {builtup['Avg_NDBI']:.3f})

Key Observation:

Districts with lower vegetation cover
generally show higher temperatures,
while increased built-up intensity
correlates with stronger urban heat effects.
""")

# ==================================
# DATA COVERAGE
# ==================================

st.write("---")

st.header("📍 Data Coverage")

st.success("""
Study Area:
Delhi, India

Districts Analysed:
9

Satellite Sources:
• Landsat 8 Collection 2
• Sentinel-2 Harmonized

Indicators:
• Land Surface Temperature (LST)
• Normalized Difference Vegetation Index (NDVI)
• Normalized Difference Built-up Index (NDBI)
""")
