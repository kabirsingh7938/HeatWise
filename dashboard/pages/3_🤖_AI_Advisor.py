import streamlit as st
import pandas as pd
import google.generativeai as genai
from pathlib import Path

st.set_page_config(
    page_title="AI Advisor",
    page_icon="🤖",
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

avg_temp = df["Avg_LST"].mean()
avg_ndvi = df["Avg_NDVI"].mean()
avg_ndbi = df["Avg_NDBI"].mean()

# ==================================
# GEMINI CONFIG
# ==================================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

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
# HEATWISE COPILOT
# ==================================

st.write("---")

st.subheader("🤖 HeatWise Urban Climate Copilot")

question = st.text_area(
    "Ask HeatWise",
    placeholder="Why is South West Delhi hotter than New Delhi?"
)

if st.button("Generate AI Insight"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Analyzing urban heat intelligence..."):

            prompt = f"""
You are HeatWise AI.

You are an expert urban climate analyst helping city planners understand heat stress.

Selected District:
{district}

District Metrics:
Temperature (LST): {district_data['Avg_LST']:.2f} °C
NDVI: {district_data['Avg_NDVI']:.3f}
NDBI: {district_data['Avg_NDBI']:.3f}

Delhi Averages:
Temperature: {avg_temp:.2f} °C
NDVI: {avg_ndvi:.3f}
NDBI: {avg_ndbi:.3f}

Instructions:

- Explain findings clearly.
- Use district data when relevant.
- Recommend cooling interventions.
- Explain NDVI and NDBI when useful.
- Provide practical urban planning insights.
- Answer in a professional but easy-to-understand way.

User Question:

{question}
"""

            try:

                response = model.generate_content(
                    prompt
                )

                st.success(
                    response.text
                )

            except Exception as e:

                st.error(
                    f"Gemini Error: {e}"
                )

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
• Why is South West Delhi hotter than New Delhi?

• Which district should receive cooling investments first?

• What would happen if NDVI increased by 20%?

• How can Delhi reduce urban heat island effects?

• Explain this district's heat risk.

• What cooling strategy is best for this district?

• Compare this district with the coolest district.

• How does built-up intensity affect temperature?
""")
