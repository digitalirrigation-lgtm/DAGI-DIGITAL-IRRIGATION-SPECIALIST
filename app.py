import streamlit as st
import ee
import folium
from streamlit_folium import st_folium

# ----------------------------
# PAGE TITLE
# ----------------------------
st.title("🌱 Irrigation Intelligence Dashboard")

# ----------------------------
# EARTH ENGINE AUTH (STREAMLIT CLOUD SAFE)
# ----------------------------
# IMPORTANT:
# You will later add credentials in Streamlit Cloud "Secrets"
# For now this prevents crashing during setup testing

try:
    service_account = st.secrets["service_account"]
    private_key = st.secrets["private_key"]

    credentials = ee.ServiceAccountCredentials(
        service_account,
        key_data=private_key
    )

    ee.Initialize(credentials)

    st.success("Earth Engine Connected ✅")

except Exception as e:
    st.warning("Earth Engine not connected yet. Add secrets in Streamlit Cloud.")
    st.stop()

# ----------------------------
# SENTINEL-2 NDVI
# ----------------------------
image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterDate("2024-01-01", "2024-01-31") \
    .median()

ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

# ----------------------------
# VISUALIZATION
# ----------------------------
ndvi_vis = ndvi.visualize(
    min=0,
    max=1,
    palette=['red', 'yellow', 'green']
)

# ----------------------------
# MAP
# ----------------------------
m = folium.Map(location=[9.0, 38.7], zoom_start=6)

map_id = ee.Image(ndvi_vis).getMapId()

folium.raster_layers.TileLayer(
    tiles=map_id['tile_fetcher'].url_format,
    attr="Google Earth Engine",
    name="NDVI",
    overlay=True,
    control=True
).add_to(m)

st_folium(m, width=700, height=500)
