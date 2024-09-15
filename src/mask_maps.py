import geopandas as gpd
import rasterio
import os
from osgeo import gdal
from rasterio.mask import mask
import matplotlib.pyplot as plt
from tqdm import tqdm
from joblib import Parallel, delayed

# dej na false jestli neni potreba zobrazovat kropnuty data
DEBUG_SHOW = False

GEOJSON_DIR = '../dataset/geojson'
OUTPUT_DIR = '../dataset/out2012'
# CLC_MAP_TIF = '../dataset/clc/CLCplus_2018_010m.tif'
TREES_MAP_TIF = '../dataset/trees-density/TCD_2012_020m_03035_d03.tif'

# predpokladej, ze zipy jsou v dataset/shp
SHP_DIR = '/home/basta/shp/ku/epsg-5514'
CADASTRE_FILE = "KATASTRALNI_UZEMI_P.shp"

def mask_maps(cadastre_number, cadastre_path):

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


    gdf = gpd.read_file(cadastre_path)
    gdf = gdf.to_crs(epsg=3035)

    # splacej stromy
    # with rasterio.open(CLC_MAP_TIF) as src:
    #     out_image, out_transform = mask(src, gdf.geometry, crop=True)
    #
    #     # Update the metadata for the new file
    #     out_meta = src.meta.copy()
    #     out_meta.update({
    #         "driver": "GTiff",
    #         "height": out_image.shape[1],
    #         "width": out_image.shape[2],
    #         "transform": out_transform
    #     })
    #
    #     outfile = OUTPUT_DIR + "/" + cadastre_number + "-CLC.tif"
    #     _save_new_tif(outfile, out_meta)
    #     if (DEBUG_SHOW):
    #         _debug_show(outfile)

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

        outfile = OUTPUT_DIR + "/" + cadastre_number + "-TREES.tif"
        _save_new_tif(outfile, out_meta)
        if (DEBUG_SHOW):
            _debug_show(outfile)


def list_directories(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs

if __name__ == "__main__":
    # projed vsechny adresare

    directories = list_directories(SHP_DIR)

    def process_directory(d):
        cadastre_path = SHP_DIR + "/" + d + f"/{d}" + "/" + CADASTRE_FILE
        if os.path.isfile(cadastre_path):
            mask_maps(d, cadastre_path)
        else:
            print(d, "not found, skipping")


    # Parallelize the process
    Parallel(n_jobs=-1)(delayed(process_directory)(d) for d in tqdm(directories))

