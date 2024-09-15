import ee
import geemap
import os

# Initialize Earth Engine
ee.Initialize()

# Define the area of interest (Prague)
prague = ee.Geometry.Point(14.4378, 50.0755).buffer(20000)

# Define the time range
start_date = '2020-7-01'
end_date = '2021-12-31'

# Select the Sentinel-2 Surface Reflectance dataset
collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
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
    for year in range(2022, 2023)
    for month in range(7, 13)
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

# Optionally, use geemap to visualize a composite
Map = geemap.Map()
Map.centerObject(prague, 9)
Map.addLayer(monthly_composites.first(), {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'RGB Composite')
Map.to_streamlit()
