from osgeo import gdal
import matplotlib.pyplot as plt
import rasterio
from rasterio import CRS
from rasterio.coords import BoundingBox
from rasterio.plot import show
from rasterio.warp import transform_bounds, transform

if __name__ == "__main__":
    FILE = "TCD_2018_010m_03035_V2_0.tif"

    with rasterio.open(FILE) as src:
        print(src.width, src.height)
        print(src.bounds)
        print(src.crs.data)

        bbox = BoundingBox(*transform_bounds(src.crs, CRS.from_epsg(5514), *src.bounds))
        print(bbox)

        data = src.read(1)
        print(data.shape)

        # window = src.window(*src.bounds)
        # print(window)

        # plt.imshow(src)
        # plt.show()
        # show(src)
