import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Forecast",
    page_icon="🔮",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================

from pathlib import Path

csv_file = Path(__file__).resolve().parents[2] / "data" / "HeatWise_Delhi_District_Intelligence.csv"
df = pd.read_csv(csv_file)

df.columns = df.columns.str.strip()

# ==================================
# PAGE HEADER
# ==================================

st.title("🔮 HeatWise Forecast Engine")

st.markdown("""
District-level urban heat forecasting
based on current HeatWise intelligence.
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

current_temp = district_data["Avg_LST"]

# ==================================
# FORECAST SETTINGS
# ==================================

years = st.slider(
    "Forecast Horizon (Years)",
    1,
    20,
    10
)

annual_increase = st.slider(
    "Expected Annual Warming (°C)",
    0.1,
    1.0,
    0.35
)

# ==================================
# FORECAST CALCULATION
# ==================================

forecast_years = list(
    range(2025, 2025 + years + 1)
)

temps = []

for i in range(len(forecast_years)):

    projected = current_temp + (
        i * annual_increase
    )

    temps.append(
        round(projected, 2)
    )

forecast_df = pd.DataFrame({
    "Year": forecast_years,
    "Projected Temperature": temps
})

# ==================================
# METRICS
# ==================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "District",
        district
    )

with c2:
    st.metric(
        "Current Temp",
        f"{current_temp:.2f} °C"
    )

with c3:
    st.metric(
        "Forecast Horizon",
        f"{years} Years"
    )

with c4:
    st.metric(
        "Projected Increase",
        f"+{temps[-1]-temps[0]:.2f} °C"
    )

# ==================================
# CHART
# ==================================

st.write("---")

st.subheader(
    f"📈 Temperature Forecast: {district}"
)

st.line_chart(
    forecast_df.set_index("Year")
)

# ==================================
# TABLE
# ==================================

st.write("---")

st.subheader("Forecast Dataset")

st.dataframe(
    forecast_df,
    use_container_width=True
)

# ==================================
# AI INSIGHT
# ==================================

st.write("---")

st.subheader("🤖 AI Forecast Assessment")

increase = temps[-1] - temps[0]

if increase > 5:

    st.error(
        f"""
Severe warming trend projected for {district}.

Recommended Actions:

• Expand tree canopy

• Cool roof programs

• Urban greening

• Heat-resilient planning
"""
    )

elif increase > 2:

    st.warning(
        f"""
Moderate warming trend projected for {district}.

Recommended Actions:

• Increase vegetation

• Improve shaded infrastructure

• Monitor heat exposure
"""
    )

else:

    st.success(
        f"""
Relatively stable temperature trend projected for {district}.
"""
    )

# ==================================
# DISTRICT COMPARISON
# ==================================

st.write("---")

st.subheader("🔥 Current District Heat Ranking")

ranking = df.sort_values(
    "Avg_LST",
    ascending=False
)

display_df = ranking[
    [
        "DISTRICT",
        "Avg_LST",
        "Avg_NDVI",
        "Avg_NDBI"
    ]
].copy()

display_df.columns = [
    "District",
    "Temperature (°C)",
    "Vegetation Index",
    "Built-up Index"
]

st.dataframe(
    display_df,
    use_container_width=True
)
