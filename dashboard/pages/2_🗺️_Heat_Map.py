import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Heat Map",
    page_icon="🗺",
    layout="wide"
)

# ==================================
# LOAD DISTRICT DATA
# ==================================

df = pd.read_csv("../data/HeatWise_Delhi_District_Intelligence.csv")

df.columns = df.columns.str.strip()

# ==================================
# HEAT CLASSIFICATION
# ==================================

def classify_heat(temp):

    if temp > 48:
        return "High"

    elif temp > 45:
        return "Moderate"

    else:
        return "Low"


df["HeatClass"] = df["Avg_LST"].apply(classify_heat)

# ==================================
# SUMMARY
# ==================================

avg_temp = df["Avg_LST"].mean()

hottest = df.loc[df["Avg_LST"].idxmax()]
coolest = df.loc[df["Avg_LST"].idxmin()]

# ==================================
# HEADER
# ==================================

st.title("🗺 Delhi District Heat Map")

st.markdown("""
District-level urban heat intelligence
generated from satellite imagery and AI analysis.
""")

# ==================================
# METRICS
# ==================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Districts",
        len(df)
    )

with c2:
    st.metric(
        "Avg Temperature",
        f"{avg_temp:.2f} °C"
    )

with c3:
    st.metric(
        "🔥 Hottest",
        hottest["DISTRICT"]
    )

with c4:
    st.metric(
        "🌡 Coolest",
        coolest["DISTRICT"]
    )

st.write("---")

# ==================================
# DISTRICT TABLE
# ==================================

st.subheader("District Heat Intelligence")

display_df = df[
    [
        "DISTRICT",
        "Avg_LST",
        "Avg_NDVI",
        "Avg_NDBI",
        "HeatClass"
    ]
].sort_values(
    "Avg_LST",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True
)

# ==================================
# HEAT RANKINGS
# ==================================

st.write("---")

st.subheader("🔥 Heat Rankings")

for i, row in enumerate(
    display_df.head(9).itertuples(),
    start=1
):

    if row.HeatClass == "High":
        st.error(
            f"{i}. {row.DISTRICT} — {row.Avg_LST:.2f} °C"
        )

    elif row.HeatClass == "Moderate":
        st.warning(
            f"{i}. {row.DISTRICT} — {row.Avg_LST:.2f} °C"
        )

    else:
        st.success(
            f"{i}. {row.DISTRICT} — {row.Avg_LST:.2f} °C"
        )

# ==================================
# VISUAL MAP
# ==================================

st.write("---")

st.subheader("Delhi District Risk Overview")

m = folium.Map(
    location=[28.61, 77.20],
    zoom_start=10,
    tiles="CartoDB dark_matter"
)

district_locations = {
    "Central": [28.65, 77.23],
    "East": [28.63, 77.30],
    "New Delhi": [28.61, 77.21],
    "North": [28.73, 77.20],
    "North East": [28.72, 77.27],
    "North West": [28.79, 77.11],
    "South": [28.53, 77.24],
    "South West": [28.58, 77.05],
    "West": [28.66, 77.10]
}

for _, row in df.iterrows():

    district = row["DISTRICT"]

    if district not in district_locations:
        continue

    if row["HeatClass"] == "High":
        color = "red"

    elif row["HeatClass"] == "Moderate":
        color = "orange"

    else:
        color = "green"

    folium.CircleMarker(
        location=district_locations[district],
        radius=12,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=f"""
        <b>{district}</b><br>
        Temperature: {row['Avg_LST']:.2f} °C<br>
        NDVI: {row['Avg_NDVI']:.3f}<br>
        NDBI: {row['Avg_NDBI']:.3f}
        """
    ).add_to(m)

st_folium(
    m,
    width=1200,
    height=650
)

# ==================================
# LEGEND
# ==================================

st.write("---")

st.info("""
🔴 High Heat Risk (>48°C)

🟠 Moderate Heat Risk (45–48°C)

🟢 Lower Heat Risk (<45°C)

HeatWise District Intelligence Engine
""")