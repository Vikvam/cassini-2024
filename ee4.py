import streamlit as st
import geemap
import ee
s2_collection: ee.ImageCollection = None
prague = None

start_int = 2020
end_int = 2023
# Get Sentinel-2 imagery for the selected year
start_date = f'{start_int}-01-01'
end_date = f'{end_int}-12-31'
@st.cache_data
def expensive_initialization():
    global prague
    print("Initializing...")
    global s2_collection
    try:
        ee.Initialize()
    except Exception as e:
        ee.Authenticate()
        ee.Initialize()

    prague = ee.Geometry.Point(14.4378, 50.0755).buffer(10000)
    s2_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterBounds(prague) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))


# expensive_initialization()
def main():
    st.title("Prague Yearly Maps")

    # Add sidebar for user inputs
    # year = st.sidebar.slider("Select Year", 2021, 2022, 2023)
    year = 2021

    # Create a map
    m = geemap.Map()
    m.add_basemap("HYBRID")

    # Call function to update map based on user input
    # update_map(m, year)

    # Add the map to the Streamlit app
    m.to_streamlit(height=600)

def update_map(m: geemap.Map, year):
    # Define the area of interest (Prague)
    # Create a median composite
    composite: ee.Image = s2_collection.filter(ee.Filter.calendarRange(year, year, 'year')).median()

    # Select RGB bands and clip to Prague area
    rgb_image = composite.select(['B4', 'B3', 'B2']).clip(prague)

    # Set visualization parameters
    vis_params = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}

    # Add the layer to the map
    m.addLayer(rgb_image, vis_params, f'Prague {year}')

    print(rgb_image)

    # Center the map on Prague
    m.centerObject(prague, 10)

if __name__ == "__main__":
    main()
