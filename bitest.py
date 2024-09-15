import streamlit as st
import geemap
import ee

# Initialize Earth Engine
ee.Initialize()

# Create a map centered on a location
map = geemap.Map(center=[40, -100], zoom=4)

# Add Earth Engine dataset
dem = ee.Image('USGS/SRTMGL1_003')
vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
}
map.addLayer(dem, vis_params, 'SRTM DEM')

# Create Streamlit app
st.title("Interactive Elevation Map")

geemap.use_folium()
# Display the map

map.to_streamlit()

# Get clicked location
# if map_component.last_clicked is not None:
#     clicked_lat = map_component.last_clicked['lat']
#     clicked_lon = map_component.last_clicked['lng']
#
#     st.write(f"Clicked location: {clicked_lat:.4f}, {clicked_lon:.4f}")
#
#     # Get elevation at clicked point
#     elevation = dem.sample(ee.Geometry.Point([clicked_lon, clicked_lat]), 30).first().get('elevation').getInfo()
#     st.write(f"Elevation at clicked point: {elevation:.2f} meters")
#
#     # Do something with the elevation data
#     if elevation > 1000:
#         st.write("This is a high elevation area!")
#     else:
#         st.write("This is a lower elevation area.")

# Add a button to reset view
if st.button("Reset View"):
    map_component.set_center(40, -100, 4)
