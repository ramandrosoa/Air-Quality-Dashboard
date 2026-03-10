# 🌿 Air Quality & Green Spaces Dashboard 

An interactive geospatial dashboard analyzing the relationship between **park proximity** and **air pollution levels** across monitoring stations in Los Angeles (2024).

---

## 📌 Project Overview

This project investigates whether proximity to green spaces (parks) correlates with lower air pollution levels in Los Angeles. Data was collected from **OpenAQ** (air quality monitoring stations) and **Google Street View** for location context. Park locations were retrieved via the **Overpass API** (OpenStreetMap).

For each monitoring station, the nearest park was identified and the distance calculated using the **Haversine formula** — a method that computes the great-circle distance between two points on a sphere given their latitude and longitude.

Pollution metrics analyzed:
- **PM2.5** — Fine particulate matter (µg/m³)
- **PM10** — Coarse particulate matter (µg/m³)
- **NO₂** — Nitrogen dioxide (µg/m³)

---

## 📊 Dashboard Features

- **Interactive Folium map** — monitoring stations color-coded by PM2.5 level, green space markers, and toggleable filter layers (Good / Moderate / Unhealthy)
- **KPI cards** — total stations, average PM2.5, PM10, NO₂, and park/pollution correlation
- **Scatter plot** — distance to nearest park vs PM2.5 with trendline
- **Near vs Far comparison** — average PM2.5 for stations near parks (<2km) vs far (>8km)
- **Filterable station table** — filter by PM2.5 level (Good / Moderate / Unhealthy)




---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white)
![matplotlib](https://img.shields.io/badge/matplotlib-11557C?logo=python&logoColor=white)
![seaborn](https://img.shields.io/badge/seaborn-4C72B0?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?logo=python&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?logo=render&logoColor=black)

---


## 📍 Data Sources

- **Air quality data** — [OpenAQ](https://openaq.org/) · Los Angeles monitoring stations · January–December 2024
- **Park locations** — [OpenStreetMap](https://www.openstreetmap.org/) via Overpass API
- **Location context** — Google Street View API

---

## 📝 Notes

- `static/map.html` is not included in the repository as it is generated at runtime by `generate_map.py`. On deployment, this is handled automatically in the build step.
- Stations with identical or near-identical coordinates are slightly offset on the map using a circular displacement algorithm to ensure all markers remain individually clickable.
- Each station is labeled based on its PM2.5 reading: stations at or below 12 µg/m³ are classified as **Good**, between 12 and 35 µg/m³ as **Moderate**, and above 35 µg/m³ as **Unhealthy**. These labels are used consistently across the map markers, the filter layers, and the station table.
