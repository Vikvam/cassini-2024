import glob
import json

import ee
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import geemap.foliumap as geemap
import geopandas as gpd
from folium import raster_layers
import matplotlib.colors as colors
import geemap.colormaps as cm
import src.compute_coverage
import src.potential_coverage_area

css='''
<style>
    section.main>div {
        padding-bottom: 1rem;
    }
    [data-testid="column"]:nth-of-type(2) {
    height: 700px;
    overflow: scroll;
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

INTERESTING_SHAPE_LAYERS = [
    "KATASTRALNI_UZEMI_P",
    ""

]

SHAPE_ROOT = "/home/basta/shp/ku/epsg-5514"
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

    return s2_collection, prague, pd.read_csv('shapedata.csv')


s2_collection, prague, shape_df = expensive_initialization()

# Create a map object
m = geemap.Map()

# Add a basemap
# m.add_basemap("HYBRID")
# cmap = colors.LinearSegmentedColormap.from_list("greencmapmine", ["darkgreen", "green"])

m.add_raster("transparent_treese2018.tif", layer_name="Tree coverage 2018",
             use_image_bounds=True, nodata=0, opacity=1, colormap="Greens", visible=False)
m.add_raster("transparent_treese2015.tif", layer_name="Tree coverage 2015",
             use_image_bounds=True, nodata=0, opacity=1, colormap="Greens")
m.add_raster("transparent_treese2012.tif", layer_name="Tree coverage 2012",
             use_image_bounds=True, nodata=0, opacity=1, colormap="Greens", )


if not "center" in st.session_state:
    st.session_state.center = [50.0755, 14.4378]


def location_selected(location: str):
    fname = shape_df[location == shape_df["description"]].iloc[0]["filename"]
    shapefile = f"{SHAPE_ROOT}/" + fname.replace(".zip", "") + "/" + fname.replace(".zip",
                                                                                   "") + "/KATASTRALNI_UZEMI_P.shp"
    print("Shapefile: ", shapefile)
    for shpfile in glob.glob(f"{SHAPE_ROOT}/" + fname.replace(".zip", "") + "/" + fname.replace(".zip","") + "/*.shp"):
        if "KATASTRALNI_UZEMI_P" in shpfile:
            continue
        name = shpfile.split("/")[-1].replace(".shp", "")
        if name in INTERESTING_SHAPE_LAYERS:
            m.add_
            m.add_shapefile(shpfile, layer_name=shpfile.split("/")[-1].replace(".shp", ""))

    m.add_shapefile(shapefile, layer_name="Shapefile Layer")
    gdf = gpd.read_file(shapefile)
    gdf = gdf.to_crs(epsg=4326)
    st.session_state.center = gdf["geometry"].centroid.x[0], gdf["geometry"].centroid.y[0]


def show_df(df):
    # Rename columns
    st.title("Land Coverage Analysis")
    df.columns = [
        'Urban Green Space Coverage (%)',
        'Urban Green Space Area (km²)',
        'Urban Tree Canopy Cover (%)',
        'Urban Tree Canopy Area (km²)',
        'Precise Urban Tree Canopy Coverage (%)',
        'Precise Urban Tree Canopy Area (km²)',
        'Building Coverage (%)',
        'Building Area Covered (km²)'
    ]
    st.area_chart(df.iloc[:, [1, 3, 7]])

    # Format percentage columns
    percentage_columns = ['Urban Green Space Coverage (%)', 'Urban Tree Canopy Cover (%)', 'Precise Urban Tree Canopy Coverage (%)',
                          'Building Coverage (%)']
    for col in percentage_columns:
        df[col] = df[col].apply(lambda x: f"{x:.2%}")

    # Format area columns
    area_columns = ['Urban Green Space Area (km²)', 'Urban Tree Canopy Area (km²)', 'Precise Urban Tree Canopy Area (km²)', 'Building Area Covered (km²)']
    for col in area_columns:
        df[col] = df[col].apply(lambda x: f"{x:,.0f}")

    # Streamlit app

    st.write("This table shows the breakdown of land coverage in our region:")

    # Use st.dataframe with custom styling
    st.dataframe(
        df.style.set_properties(**{'background-color': '#f0f2f6', 'color': '#1e1e1e', 'border-color': '#ffffff'})
        .set_table_styles([{'selector': 'th', 'props': [('background-color', '#0E1117'), ('color', '#0E1117')]}])
        .format(precision=2)
    )

    # Add some explanatory text
    st.write("""
    * **Urban Green Space Coverage**: Represents the percentage and area of grassland.
    * **Urban Tree Canopy Coverage**: Shows the overall tree coverage.
    * **Precise Urban Tree Canopy Coverage**: Indicates a more accurate measurement of tree coverage.
    * **Building Coverage**: Represents the percentage and area covered by buildings.
    """)


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
    # m.addLayer(rgb_image, vis_params, f'Prague {year}')

    print("Centering on", st.session_state.center)
    m.centerObject(ee.Geometry.Point(st.session_state.center).buffer(5000), 15)

def draw_gdfs(gdfs):
    for gdf in gdfs:
        m.add_gdf(gdf, layer_name=gdf["ID"].iloc[0])

col1, col2 = st.columns([1, 1])
with col1:
    selection = st.selectbox("Select location", options=shape_df["description"].tolist(), index=0)
    location_selected(selection)
    update_map(m, 2023, 0.5)
    draw_gdfs(src.potential_coverage_area.get_gdfs_for_code(selection.split("[")[-1][:-1]))
    m.to_streamlit(bidirectional=False)

with col2:
    show_df(src.compute_coverage.compute_cov_id(selection.split("[")[-1][:-1], "2018"))

# Display the map
