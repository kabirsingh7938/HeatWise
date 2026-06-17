\# HeatWise: AI/ML Urban Heat Assessment of Delhi



\## Project Overview



HeatWise is an Urban Heat Island assessment project that combines remote sensing and machine learning to understand how vegetation and built-up areas influence land surface temperature (LST) across Delhi.



\---



\## Objectives



\- Analyze Land Surface Temperature (LST)

\- Measure vegetation using NDVI

\- Measure built-up intensity using NDBI

\- Study relationships between environmental variables

\- Predict temperature using machine learning



\---



\## Data Sources



\### Landsat 8

Used for Land Surface Temperature extraction.



\### Sentinel-2

Used for NDVI and NDBI calculations.



\### FAO GAUL Administrative Boundaries

Used to obtain Delhi boundary.



\---



\## Methodology



\### Feature Extraction



1\. LST from Landsat 8 thermal band

2\. NDVI = (NIR - Red) / (NIR + Red)

3\. NDBI = (SWIR - NIR) / (SWIR + NIR)



\### Sampling



5000 random sample points generated across Delhi.



\### Machine Learning



Model Used:

\- Random Forest Regressor



Target:

\- LST



Predictors:

\- NDVI

\- NDBI



\---



\## Results



\### Correlation Analysis



NDVI vs LST Correlation:



\-0.448



Interpretation:

Higher vegetation is associated with lower temperatures.



\### Feature Importance



NDBI Importance: 0.683



NDVI Importance: 0.317



Interpretation:

Built-up intensity has stronger influence on temperature than vegetation.



\### Model Performance



R² Score: 0.539



MAE: 2.04 °C



Interpretation:

The model explains approximately 54% of temperature variation.



\---



\## Key Findings



\- Vegetation reduces urban heat.

\- Built-up regions exhibit higher temperatures.

\- NDBI is the strongest predictor of LST.

\- Machine learning can effectively estimate urban temperature patterns.



\---



\## Future Improvements



\- Add population density data.

\- Add night-time light data.

\- Use XGBoost and Gradient Boosting.

\- Generate ward-level heat vulnerability maps.

\- Develop a web dashboard.



\---



\## Author



Kabir Singh



HeatWise v1

