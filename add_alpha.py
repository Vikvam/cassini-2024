import rasterio
import numpy as np

# Open the raster file
with rasterio.open('dataset/trees-density/TCD_2018_010m_03035_V2_0.tif') as src:
    # Read the raster data
    data = src.read()

    # Create an alpha band
    alpha = np.full(data.shape[1:], 255, dtype=rasterio.uint8)

    # Adjust the values in the alpha band based on the values in the raster data
    # Pixels with higher values will be less transparent
    alpha[data[0] < data[0].mean()] = 0

    # Add the alpha band to the raster data
    data_with_alpha = np.concatenate((data, alpha[None, :, :]))

    # Define the new raster's profile
    profile = src.profile
    profile.update(count=src.count+1, dtype=rasterio.uint8)

    # Write the raster data with the new alpha band to a new raster file
    with rasterio.open('transparent_treese.tif', 'w+', **profile) as dst:
        dst.write(data_with_alpha)
