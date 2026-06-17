import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cooling Simulator",
    page_icon="🌳",
    layout="wide"
)

# ==================================
# LOAD DISTRICT DATA
# ==================================

df = pd.read_csv(
    "../data/HeatWise_Delhi_District_Intelligence.csv"
)

df.columns = df.columns.str.strip()

# ==================================
# PAGE HEADER
# ==================================

st.title("🌳 HeatWise Cooling Simulator")

st.markdown("""
Simulate how urban interventions can reduce
district-level temperatures across Delhi.
""")

# ==================================
# DISTRICT SELECTION
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
# USER INPUTS
# ==================================

tree_cover = st.slider(
    "Increase Tree Cover (%)",
    0,
    50,
    10
)

green_roofs = st.slider(
    "Green Roof Adoption (%)",
    0,
    50,
    10
)

cool_roofs = st.slider(
    "Cool Roof Adoption (%)",
    0,
    50,
    10
)

# ==================================
# AI COOLING MODEL
# ==================================

tree_cooling = tree_cover * 0.12
green_roof_cooling = green_roofs * 0.08
cool_roof_cooling = cool_roofs * 0.06

total_cooling = (
    tree_cooling +
    green_roof_cooling +
    cool_roof_cooling
)

future_temp = max(
    current_temp - total_cooling,
    25
)

# ==================================
# METRICS
# ==================================

st.write("---")

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
        "Cooling Impact",
        f"-{total_cooling:.2f} °C"
    )

with c4:
    st.metric(
        "Projected Temp",
        f"{future_temp:.2f} °C"
    )

# ==================================
# IMPACT BREAKDOWN
# ==================================

st.write("---")

st.subheader("📊 Cooling Contribution")

impact_df = pd.DataFrame({
    "Strategy": [
        "Tree Cover",
        "Green Roofs",
        "Cool Roofs"
    ],
    "Cooling Effect": [
        tree_cooling,
        green_roof_cooling,
        cool_roof_cooling
    ]
})

st.bar_chart(
    impact_df.set_index(
        "Strategy"
    )
)

# ==================================
# AI RECOMMENDATION
# ==================================

st.write("---")

st.subheader("🤖 AI Recommendation")

if total_cooling > 8:

    st.success(f"""
Excellent cooling strategy for {district}.

This intervention package could significantly
reduce urban heat and improve thermal comfort.
""")

elif total_cooling > 4:

    st.warning(f"""
Moderate cooling impact projected for {district}.

Increasing vegetation further would provide
stronger cooling benefits.
""")

else:

    st.error(f"""
Limited cooling impact projected for {district}.

Consider larger investments in urban greenery,
green roofs, and reflective materials.
""")

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

# ==================================
# SIMULATION SUMMARY
# ==================================

st.write("---")

st.subheader("🌍 Simulation Summary")

st.info(f"""
District: {district}

Current Temperature:
{current_temp:.2f} °C

Estimated Cooling:
{total_cooling:.2f} °C

Projected Temperature:
{future_temp:.2f} °C

Tree Cover Increase:
{tree_cover}%

Green Roof Adoption:
{green_roofs}%

Cool Roof Adoption:
{cool_roofs}%
""")