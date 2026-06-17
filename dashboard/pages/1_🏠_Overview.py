import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Overview",
    page_icon="🏠",
    layout="wide"
)

# ==================================
# LOAD DISTRICT DATA
# ==================================

df = pd.read_csv("../data/HeatWise_Delhi_District_Intelligence.csv")

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

heatwise_score = int(
    100
    - (avg_temp - 40) * 2
    + avg_ndvi * 50
    - avg_ndbi * 20
)

heatwise_score = max(0, min(100, heatwise_score))

# ==================================
# HEADER
# ==================================

st.title("🏠 HeatWise Overview")

st.markdown(
    """
AI-powered urban heat intelligence platform for understanding
temperature, vegetation, and built-up impacts across Delhi.
"""
)

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
        "🔥 HeatWise Score",
        f"{heatwise_score}/100"
    )

st.write("---")

# ==================================
# HEAT RISK
# ==================================

st.subheader("AI Heat Risk Assessment")

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

st.subheader("🔥 District Intelligence")

a, b = st.columns(2)

with a:
    st.info(
        f"""
### 🔥 Hottest District

**{hottest['DISTRICT']}**

Temperature: **{hottest['Avg_LST']:.2f} °C**
"""
    )

with b:
    st.success(
        f"""
### 🌡 Coolest District

**{coolest['DISTRICT']}**

Temperature: **{coolest['Avg_LST']:.2f} °C**
"""
    )

c, d = st.columns(2)

with c:
    st.success(
        f"""
### 🌿 Greenest District

**{greenest['DISTRICT']}**

NDVI: **{greenest['Avg_NDVI']:.3f}**
"""
    )

with d:
    st.warning(
        f"""
### 🏢 Most Built-Up District

**{builtup['DISTRICT']}**

NDBI: **{builtup['Avg_NDBI']:.3f}**
"""
    )

st.write("---")

# ==================================
# TOP DISTRICTS TABLE
# ==================================

st.subheader("🏆 District Rankings")

ranking = df.sort_values(
    "Avg_LST",
    ascending=False
)[
    ["DISTRICT", "Avg_LST", "Avg_NDVI", "Avg_NDBI"]
]

st.dataframe(
    ranking,
    use_container_width=True
)

st.write("---")

# ==================================
# SUMMARY
# ==================================

st.subheader("🌍 HeatWise Summary")

st.info(
    f"""
Delhi Average Temperature: {avg_temp:.2f} °C

Hottest District: {hottest['DISTRICT']}

Coolest District: {coolest['DISTRICT']}

Greenest District: {greenest['DISTRICT']}

Most Built-Up District: {builtup['DISTRICT']}

HeatWise now uses district-level satellite intelligence
instead of anonymous sample points.
"""
)