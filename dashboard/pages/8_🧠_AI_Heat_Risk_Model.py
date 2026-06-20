import streamlit as st
import pandas as pd
from pathlib import Path

from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="AI Heat Risk Model",
    page_icon="🧠",
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
# CREATE HEAT RISK SCORE
# ==================================

df["Heat_Risk_Score"] = (
    (df["Avg_LST"] * 2)
    - (df["Avg_NDVI"] * 50)
    + (df["Avg_NDBI"] * 100)
)

# Normalize to 0–100

min_score = df["Heat_Risk_Score"].min()
max_score = df["Heat_Risk_Score"].max()

df["Heat_Risk_Score"] = (
    (
        df["Heat_Risk_Score"] - min_score
    )
    /
    (
        max_score - min_score
    )
) * 100

# ==================================
# TRAIN ML MODEL
# ==================================

X = df[
    [
        "Avg_LST",
        "Avg_NDVI",
        "Avg_NDBI"
    ]
]

y = df["Heat_Risk_Score"]

model = LinearRegression()

model.fit(X, y)

predictions = model.predict(X)

df["Predicted_Risk"] = predictions

# ==================================
# PAGE HEADER
# ==================================

st.title("🧠 AI Heat Risk Prediction Model")

st.markdown("""
Machine learning model that predicts
district heat risk using:

• Land Surface Temperature (LST)

• Vegetation Index (NDVI)

• Built-up Index (NDBI)

This aligns with the AI/ML modelling
objective of HeatWise.
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

risk = district_data["Predicted_Risk"]

# ==================================
# MAIN METRICS
# ==================================

st.write("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Temperature",
        f"{district_data['Avg_LST']:.2f} °C"
    )

with c2:
    st.metric(
        "NDVI",
        f"{district_data['Avg_NDVI']:.3f}"
    )

with c3:
    st.metric(
        "NDBI",
        f"{district_data['Avg_NDBI']:.3f}"
    )

with c4:
    st.metric(
        "Predicted Heat Risk",
        f"{risk:.1f}/100"
    )

# ==================================
# RISK LEVEL
# ==================================

st.write("---")

st.subheader("🔥 AI Risk Assessment")

if risk >= 75:

    st.error(
        "High Heat Risk District"
    )

elif risk >= 50:

    st.warning(
        "Moderate Heat Risk District"
    )

else:

    st.success(
        "Low Heat Risk District"
    )

# ==================================
# FEATURE IMPORTANCE
# ==================================

st.write("---")

st.subheader("📊 AI Feature Importance")

coefficients = pd.DataFrame({
    "Factor": [
        "Temperature (LST)",
        "Vegetation (NDVI)",
        "Built-up (NDBI)"
    ],
    "Impact": [
        abs(model.coef_[0]),
        abs(model.coef_[1]),
        abs(model.coef_[2])
    ]
})

coefficients["Impact"] = (
    coefficients["Impact"]
    /
    coefficients["Impact"].sum()
) * 100

st.bar_chart(
    coefficients.set_index(
        "Factor"
    )
)

# ==================================
# EXPLAINABLE AI
# ==================================

st.write("---")

st.subheader("🧠 Explainable AI")

top_factor = coefficients.sort_values(
    "Impact",
    ascending=False
).iloc[0]["Factor"]

st.info(
    f"""
Predicted Heat Risk: {risk:.1f}/100

Most Influential Factor:

{top_factor}

HeatWise uses machine learning to
identify how temperature, vegetation,
and built-up intensity contribute to
urban heat stress.
"""
)

# ==================================
# DISTRICT RISK RANKING
# ==================================

st.write("---")

st.subheader("🏆 Heat Risk Rankings")

ranking = df.sort_values(
    "Predicted_Risk",
    ascending=False
)

display_df = ranking[
    [
        "DISTRICT",
        "Predicted_Risk",
        "Avg_LST",
        "Avg_NDVI",
        "Avg_NDBI"
    ]
].copy()

display_df.columns = [
    "District",
    "Predicted Risk",
    "Temperature (°C)",
    "Vegetation Index",
    "Built-up Index"
]

st.dataframe(
    display_df,
    use_container_width=True
)

# ==================================
# MODEL SUMMARY
# ==================================

st.write("---")

st.subheader("🎯 AI Model Summary")

st.success("""
HeatWise AI Model

Inputs:
• Land Surface Temperature
• Vegetation Index
• Built-up Index

Output:
• Predicted Heat Risk Score

Purpose:
• Identify vulnerable districts
• Support cooling intervention planning
• Enable data-driven urban resilience strategies
""")
