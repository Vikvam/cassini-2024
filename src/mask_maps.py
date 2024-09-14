import geopandas as gpd
import rasterio
from osgeo import gdal
from rasterio.mask import mask
import matplotlib.pyplot as plt

# dej na false jestli neni potreba zobrazovat kropnuty data
DEBUG_SHOW = False

GEOJSON_DIR = '../dataset/geojson'
OUTPUT_DIR = '../dataset/out'
CLC_MAP_TIF = '../dataset/clc/CLCplus_2018_010m.tif'
TREES_MAP_TIF = '../dataset/trees-density/TCD_2018_010m_03035_V2_0.tif'

# json_name zadavat bez .json!!!!!!!!!!!!!!
def mask_maps(json_name):

    def _save_new_tif(filename, out_meta):
        with rasterio.open(outfile, 'w', **out_meta) as dest:
            dest.write(out_image)

    def _debug_show(filename):
        dataset = gdal.Open(filename)
        # Get raster band (e.g., first band)
        band = dataset.GetRasterBand(1)

        # Read raster data
        data = band.ReadAsArray()
        plt.imshow(data, cmap='gray')
        plt.colorbar()  # To show the color scale
        plt.title('GeoTIFF Image')
        plt.show()
        

    geojson_path = GEOJSON_DIR + "/" + json_name + ".json"
    gdf = gpd.read_file(geojson_path)

    # splacej stromy
    with rasterio.open(CLC_MAP_TIF) as src:
        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        
        # Update the metadata for the new file
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        outfile = OUTPUT_DIR + "/" + json_name + "-CLC.tif"
        _save_new_tif(outfile, out_meta)
        if (DEBUG_SHOW):
            _debug_show(outfile)

    # splacej vsechno lmbao
    with rasterio.open(TREES_MAP_TIF) as src:
        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        
        # Update the metadata for the new file
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        outfile = OUTPUT_DIR + json_name + "-TREES.tif"
        _save_new_tif(outfile, out_meta)
        if (DEBUG_SHOW):
            _debug_show(outfile)

if __name__ == "__main__":
    mask_maps("praha1")
