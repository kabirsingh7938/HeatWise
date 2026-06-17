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
