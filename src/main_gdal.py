from osgeo import gdal
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dataset = gdal.Open("TCD_2018_010m_cz_03035_v020/DATA/TCD_2018_010m_E44N29_03035_v020.tif", gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)
    arr = band.ReadAsArray()
    plt.imshow(arr)
    plt.show()
