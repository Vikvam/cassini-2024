import pandas as pd
import rasterio
from osgeo import gdal
from rasterio.mask import mask
import matplotlib.pyplot as plt
import os
import numpy as np
import json
import rasterio

ROOT = "./dataset/"
ROOT2 = "../dataset/"


def compute_cov(file_tree, file_clc):
    building = [1]
    trees = [2, 3, 4]
    grass = [5, 6, 10]
    RASTER = 1 / 10000  # m

    with rasterio.open(file_clc) as src:
        data = src.read(1)
        tree_cov = np.sum([np.sum(data == x) for x in trees])
        building_cov = np.sum([np.sum(data == x) for x in building])
        grass_cov = np.sum([np.sum(data == x) for x in grass])
        all_cov = np.sum(data != 255)

        grass_per = grass_cov / all_cov
        grass_km2 = grass_cov * RASTER

        building_per = building_cov / all_cov
        building_km2 = building_cov * RASTER

        tree_fake_per = tree_cov / all_cov
        tree_fake_km2 = tree_cov * RASTER

    with rasterio.open(file_tree) as src:
        data = src.read(1)
        tree_cov = np.sum((data != 240) * (data / 100))
        tree_per = tree_cov / all_cov
        tree_km2 = tree_cov * RASTER

    # print(file)
    # print("Grass_per: ", grass_per)
    # print("Tree_per: ", tree_fake_per)
    # print("Tree_precise_per: ", tree_per)
    # print("Builiding_per: ", building_per)

    output_J = {
        'grass_per': float(grass_per),
        'grass_km2': float(grass_km2),
        'tree_per': float(tree_fake_per),
        'tree_km2': float(tree_fake_km2),
        'tree_precise_per': float(tree_per),
        'tree_precise_km2': float(tree_km2),
        'building_per': float(building_per),
        'building_km2': float(building_km2)
    }

    return output_J


def compute_cov_id(code: str, yr: str):
    root1 = f"{ROOT}/out{yr}/"
    root2 = f"{ROOT2}/out{yr}/"
    try:
        file_tree = f"{root1}/{code}-TREES.tif"
        file_clc = f"{root1}/{code}-CLC.tif"
        data = compute_cov(file_tree, file_clc)

    except rasterio.RasterioIOError:
        file_tree = f"{root2}/{code}-TREES.tif"
        file_clc = f"{root2}/{code}-CLC.tif"
        data = compute_cov(file_tree, file_clc)

    return pd.DataFrame([data])
