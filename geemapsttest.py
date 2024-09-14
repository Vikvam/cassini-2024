import ee
import streamlit as st
import geemap.foliumap as geemap

start_int = 2020
end_int = 2023
# Get Sentinel-2 imagery for the selected year
start_date = f'{start_int}-01-01'
end_date = f'{end_int}-12-03'

def mask_trees(image: ee.Image, thresh: float):
    ndvi = image.normalizedDifference(['B8', 'B4'])
    return image.updateMask(ndvi.gt(thresh))

@st.cache_data
def expensive_initialization():
    print("Initializing...")
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

    prague = ee.Geometry.Point(14.4378, 50.0755).buffer(10000)
    s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(prague) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    return s2_collection, prague

s2_collection, prague = expensive_initialization()

st.title("Simple Geemap App")

# Create a map object
m = geemap.Map()

# Add a basemap
m.add_basemap("HYBRID")
m.add_raster("CLCplus_2018_010m.tif", layer_name="Raster Layer")

m.add_geojson("praha1_2.json", layer_name="GeoJSON Layer")


def update_map(m: geemap.Map, year, thresh):
    # Define the area of interest (Prague)
    prague = ee.Geometry.Point(14.4378, 50.0755).buffer(10000)

    # Get Sentinel-2 imagery for the selected year
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    # Create a median composite
    composite = s2_collection.median()

    # Select RGB bands and clip to Prague area
    rgb_image = composite.clip(prague)
    rgb_image = mask_trees(rgb_image, thresh)

    # Set visualization parameters
    vis_params = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}

    # Add the layer to the map
    m.addLayer(rgb_image, vis_params, f'Prague {year}')

    # Center the map on Prague
    m.centerObject(prague, 10)


year = st.sidebar.slider("Select Year", 2021, 2022, 2023)
thresh = st.sidebar.slider("Select thr", min_value=0., max_value=1., step=0.05)
update_map(m, year, thresh)

# Display the map
m.to_streamlit(width=1000, height=800)
