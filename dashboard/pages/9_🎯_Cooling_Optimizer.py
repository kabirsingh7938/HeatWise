import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Cooling Optimizer",
    page_icon="🎯",
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

st.title("🎯 HeatWise Cooling Optimizer")

st.markdown("""
AI-powered intervention optimization engine
for reducing urban heat stress.

HeatWise evaluates multiple cooling strategies
and recommends the highest-impact solution
for each district.
""")

# ==================================
# DISTRICT SELECTOR
# ==================================

district = st.selectbox(
    "Select District",
    sorted(df["DISTRICT"].unique())
)

district_data = df[
    df["DISTRICT"] == district
].iloc[0]

temp = district_data["Avg_LST"]
ndvi = district_data["Avg_NDVI"]
ndbi = district_data["Avg_NDBI"]

# ==================================
# DISTRICT OVERVIEW
# ==================================

st.write("---")

st.subheader("🏙 District Profile")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Temperature",
        f"{temp:.2f} °C"
    )

with c2:
    st.metric(
        "Vegetation (NDVI)",
        f"{ndvi:.3f}"
    )

with c3:
    st.metric(
        "Built-up (NDBI)",
        f"{ndbi:.3f}"
    )

# ==================================
# INTERVENTION ENGINE
# ==================================

tree_score = 0
coolroof_score = 0
greenroof_score = 0
water_score = 0

# Tree Planting

if ndvi < 0.25:
    tree_score += 40

if temp > 47:
    tree_score += 30

tree_score += 20

# Cool Roofs

if ndbi > 0.04:
    coolroof_score += 45

if temp > 46:
    coolroof_score += 25

coolroof_score += 15

# Green Roofs

greenroof_score += 25

if ndbi > 0.03:
    greenroof_score += 25

if temp > 45:
    greenroof_score += 20

# Water Bodies

water_score += 20

if temp > 48:
    water_score += 25

if ndvi < 0.22:
    water_score += 20

# ==================================
# COOLING IMPACT ESTIMATION
# ==================================

interventions = pd.DataFrame({
    "Intervention": [
        "🌳 Tree Planting",
        "🏠 Cool Roof Program",
        "🌿 Green Roof Program",
        "💧 Water Body Expansion"
    ],
    "Optimization Score": [
        tree_score,
        coolroof_score,
        greenroof_score,
        water_score
    ],
    "Estimated Cooling": [
        2.5,
        1.8,
        1.2,
        1.0
    ]
})

interventions = interventions.sort_values(
    "Optimization Score",
    ascending=False
)

# ==================================
# BEST RECOMMENDATION
# ==================================

st.write("---")

st.header("🥇 Recommended Intervention")

best = interventions.iloc[0]

st.success(
    f"""
Recommended Strategy:

{best['Intervention']}

Optimization Score:
{best['Optimization Score']:.0f}/100

Expected Cooling:
-{best['Estimated Cooling']:.1f} °C
"""
)

# ==================================
# RANKINGS
# ==================================

st.write("---")

st.header("🏆 Intervention Rankings")

st.dataframe(
    interventions,
    width="stretch"
)

# ==================================
# VISUALIZATION
# ==================================

st.write("---")

st.header("📊 Optimization Scores")

chart_df = interventions.set_index(
    "Intervention"
)[["Optimization Score"]]

st.bar_chart(chart_df)

# ==================================
# COMBINED STRATEGY
# ==================================

st.write("---")

st.header("🚀 Combined Strategy Simulation")

top2 = interventions.head(2)

combined_cooling = (
    top2["Estimated Cooling"].sum()
)

st.info(
    f"""
Recommended Combined Solution

1. {top2.iloc[0]['Intervention']}
2. {top2.iloc[1]['Intervention']}

Expected Cooling Impact:

-{combined_cooling:.1f} °C

This strategy provides the highest
potential reduction in urban heat
for the selected district.
"""
)

# ==================================
# PRIORITY LEVEL
# ==================================

st.write("---")

st.header("🔥 Intervention Priority")

if temp >= 48:

    st.error(
        "HIGH PRIORITY DISTRICT"
    )

elif temp >= 46:

    st.warning(
        "MODERATE PRIORITY DISTRICT"
    )

else:

    st.success(
        "LOW PRIORITY DISTRICT"
    )

# ==================================
# DECISION SUPPORT
# ==================================

st.write("---")

st.header("🧠 Decision Support Summary")

st.success(
    f"""
District: {district}

Temperature: {temp:.2f} °C

Primary Recommendation:
{best['Intervention']}

Expected Cooling:
-{best['Estimated Cooling']:.1f} °C

HeatWise AI recommends prioritizing
this intervention based on district
temperature, vegetation levels,
and built-up intensity.

This supports data-driven urban
heat mitigation planning.
"""
)
