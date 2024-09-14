import glob

from matplotlib import pyplot as plt
from osgeo import ogr
import json


def plot_layer(layer, ax):
    name = layer.GetName()
    for idx, feature in enumerate(layer):
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryName() == "POLYGON":
            points = geometry.GetGeometryRef(0)
            x = [points.GetX(j) for j in range(points.GetPointCount())]
            y = [points.GetY(j) for j in range(points.GetPointCount())]
            ax.plot(x, y, "b-", label=name if idx == 0 else None)
        elif geometry.GetGeometryName() == "POINT":
            x = geometry.GetX()
            y = geometry.GetY()
            ax.plot(x, y, "ro", label=name if idx == 0 else None)


if __name__ == "__main__":
    driver = ogr.GetDriverByName("ESRI Shapefile")

    fig, ax = plt.subplots()

    for file in glob.glob("katastr/723754/*_P.shp"):
        data = driver.Open(file, 0)
        layer = data.GetLayer()

        extent = layer.GetExtent()

        plot_layer(layer, ax)

        ax.set_xlim(min(ax.get_xlim()[0], extent[0]), max(ax.get_xlim()[1], extent[1]))
        ax.set_ylim(min(ax.get_ylim()[0], extent[2]), max(ax.get_ylim()[1], extent[3]))

    plt.legend()
    plt.show()
