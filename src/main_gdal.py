from osgeo import gdal
import matplotlib.pyplot as plt
import rasterio
from rasterio import CRS
from rasterio.coords import BoundingBox
from rasterio.warp import transform_bounds

if __name__ == "__main__":
    FILE = "TCD_2018_010m_cz_03035_v020/DATA/TCD_2018_010m_E47N30_03035_v020.tif"

    with rasterio.open(FILE) as src:
        print(src.width, src.height)
        print(src.bounds)
        print(src.crs.data)

        bbox = BoundingBox(*transform_bounds(src.crs, CRS.from_epsg(4326), *src.bounds))
        print(bbox)

        # window = src.window(*src.bounds)
        # print(window)
