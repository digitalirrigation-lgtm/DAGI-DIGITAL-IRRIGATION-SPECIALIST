import streamlit as st
import ee
import folium
from streamlit_folium import st_folium

# Initialize Earth Engine (service account method for production)
service_account = "master-robot@irrigation-intelligence-pro.iam.gserviceaccount.com"

credentials = ee.ServiceAccountCredentials(
    service_account,
    "irrigation-intelligence-pro-e2b532ddd763.json"
)

ee.Initialize(credentials)

st.title("Irrigation Intelligence Dashboard")

# Sentinel-2 NDVI
image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterDate("2024-01-01", "2024-01-31") \
    .median()

ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

ndvi_vis = ndvi.visualize(
    min=0,
    max=1,
    palette=['red', 'yellow', 'green']
)

# Map
m = folium.Map(location=[9.0, 38.7], zoom_start=6)

map_id = ee.Image(ndvi_vis).getMapId()

folium.raster_layers.TileLayer(
    tiles=map_id['tile_fetcher'].url_format,
    attr="Earth Engine",
    name="NDVI",
    overlay=True,
    control=True
).add_to(m)

st_folium(m, width=700, height=500)
