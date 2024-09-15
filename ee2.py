import ee
import geemap
import streamlit as st
import streamlit.components.v1 as components

# Initialize Earth Engine
ee.Initialize()

# Define the area of interest (Prague)
prague = ee.Geometry.Point(14.4378, 50.0755).buffer(20000)

# Define the time range
start_date = '2020-7-01'
end_date = '2021-12-31'

# Select the Sentinel-2 Surface Reflectance dataset
collection = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterBounds(prague) \
    .filterDate(start_date, end_date)

# Function to create monthly composites
def create_monthly_composite(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')
    monthly = collection.filterDate(start, end).median()
    return monthly.set('year', year).set('month', month)

# Create a list of all month/year combinations
dates = [
    (year, month)
    for year in range(2020, 2022)
    for month in range(1, 13)
]

# Create monthly composites
monthly_composites = ee.ImageCollection(
    ee.List([create_monthly_composite(year, month) for year, month in dates])
)

# Function to export an image
def export_image(image, filename):
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=filename,
        scale=10,
        region=prague,
        maxPixels=1e13
    )
    task.start()
    return task

# Export all monthly composites
tasks = []
for year, month in dates:
        image = monthly_composites.filter(ee.Filter.And(
            ee.Filter.eq('year', year),
            ee.Filter.eq('month', month)
        )).first()
        filename = f'Prague_Composite_{year}_{month:02d}'
        task = export_image(image, filename)
        tasks.append(task)

# Monitor task status
for task in tasks:
    print(f"Task {task.status()['description']}: {task.status()['state']}")

# Use geemap to visualize all composites
Map = geemap.Map()
Map.centerObject(prague, 9)

# Function to add a layer for each image
ctr = 0
def add_image_layer(image):
    global ctr
    ctr += 1
    # date = ee.Date(image.get('system:time_start'))
    # layer_name = date.format('YYYY-MM').getInfo()
    vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}
    Map.addLayer(image, vis_params, str(ctr))

# Get the list of images from the ImageCollection
image_list = monthly_composites.toList(monthly_composites.size())

# Add each image as a separate layer
for i in range(image_list.size().getInfo()):
    image = ee.Image(image_list.get(i))
    add_image_layer(image)

# Convert geemap to HTML
html_string = Map.to_html()

# Use Streamlit to display the map
st.title('Monthly Satellite Composites of Prague')
components.html(html_string, height=600)

# Add a layer control widget
Map.add_layer_control()
