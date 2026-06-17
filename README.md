\# HeatWise



AI/ML-based Urban Heat Island Assessment using Google Earth Engine and Python.



\## Objective



HeatWise analyzes the relationship between vegetation cover, built-up areas, and land surface temperature in Delhi using satellite imagery and machine learning.



\## Data Sources



\- Landsat 8 Collection 2 Level 2

\- Sentinel-2 Surface Reflectance

\- FAO GAUL Administrative Boundaries



\## Features



\- Land Surface Temperature (LST)

\- NDVI (Normalized Difference Vegetation Index)

\- NDBI (Normalized Difference Built-up Index)



\## Machine Learning



Model: Random Forest Regressor



Inputs:

\- NDVI

\- NDBI



Target:

\- LST



\## Results



\- NDVI-LST Correlation: -0.448

\- R² Score: 0.539

\- MAE: 2.04°C



\## Key Finding



Vegetation reduces urban temperatures while built-up intensity increases heat. NDBI was the strongest predictor of land surface temperature.

