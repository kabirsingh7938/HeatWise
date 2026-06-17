import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Advisor",
    page_icon="🤖",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================

df = pd.read_csv(
    "../data/HeatWise_Delhi_District_Intelligence.csv"
)

df.columns = df.columns.str.strip()

avg_temp = df["Avg_LST"].mean()
avg_ndvi = df["Avg_NDVI"].mean()
avg_ndbi = df["Avg_NDBI"].mean()

# ==================================
# PAGE
# ==================================

st.title("🤖 HeatWise AI Advisor")

st.markdown("""
Ask HeatWise about Delhi districts,
urban heat, vegetation, cooling strategies,
and climate resilience.
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

st.write("---")

st.subheader("🏙 District Intelligence")

c1, c2, c3 = st.columns(3)

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

# ==================================
# AI RECOMMENDATION
# ==================================

st.write("---")

st.subheader("🧠 AI Recommendation")

recommendation = []

if district_data["Avg_LST"] > 48:
    recommendation.append(
        "🔥 High heat risk detected."
    )
    recommendation.append(
        "Increase tree canopy coverage."
    )
    recommendation.append(
        "Deploy cool-roof programs."
    )

if district_data["Avg_NDVI"] < 0.25:
    recommendation.append(
        "🌿 Vegetation coverage is low."
    )
    recommendation.append(
        "Expand parks and green corridors."
    )

if district_data["Avg_NDBI"] > 0.04:
    recommendation.append(
        "🏢 Built-up intensity is high."
    )
    recommendation.append(
        "Promote reflective construction materials."
    )

if len(recommendation) == 0:
    recommendation.append(
        "✅ District conditions are relatively balanced."
    )

for item in recommendation:
    st.success(item)

# ==================================
# QUESTION BOX
# ==================================

st.write("---")

question = st.text_input(
    "Ask HeatWise:",
    placeholder="How can Delhi reduce urban heat?"
)

if question:

    q = question.lower()

    if "heat" in q:

        answer = f"""
Delhi average temperature is {avg_temp:.2f} °C.

The hottest district is:

{df.loc[df['Avg_LST'].idxmax()]['DISTRICT']}

Key heat drivers:

• High built-up intensity

• Low vegetation cover

• Dense urban development

Recommended actions:

• Urban forests

• Cool roofs

• Green corridors
"""

    elif "vegetation" in q or "ndvi" in q:

        answer = f"""
Average NDVI is {avg_ndvi:.3f}.

Vegetation is the strongest natural
cooling mechanism identified by HeatWise.

Districts with higher NDVI generally
show lower temperatures.
"""

    elif "building" in q or "ndbi" in q:

        answer = f"""
Average NDBI is {avg_ndbi:.3f}.

Higher NDBI indicates stronger
built-up intensity and greater
heat retention.
"""

    elif "district" in q:

        hottest = df.loc[df["Avg_LST"].idxmax()]
        coolest = df.loc[df["Avg_LST"].idxmin()]

        answer = f"""
🔥 Hottest District:
{hottest['DISTRICT']}

🌡 Coolest District:
{coolest['DISTRICT']}

HeatWise recommends prioritizing
cooling interventions in hotter districts.
"""

    elif "cooling" in q:

        answer = """
Top Cooling Strategies:

1. Urban forests

2. Green roofs

3. Cool roofs

4. Public parks

5. Water-sensitive design
"""

    else:

        answer = """
HeatWise understands:

• Heat

• Temperature

• Districts

• NDVI

• NDBI

• Vegetation

• Cooling Strategies
"""

    st.write("---")

    st.subheader("💬 HeatWise Response")

    st.success(answer)

# ==================================
# DISTRICT TABLE
# ==================================

st.write("---")

st.subheader("📊 District Intelligence Dataset")

display_df = df[
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
# SAMPLE QUESTIONS
# ==================================

st.write("---")

st.subheader("Suggested Questions")

st.info("""
• Which district is hottest?

• Which district has the most vegetation?

• How can Delhi reduce urban heat?

• What does NDVI mean?

• What does NDBI mean?

• What cooling strategy is most effective?
""")
