import rasterio
from osgeo import gdal
from rasterio.mask import mask
import matplotlib.pyplot as plt
import os
import numpy as np
import json

CLC_DIR = "clc_dir"
TREE_DIR = "tree_dir"
RASTER = 10 #m

building = [1]
trees = [2,3,4]
grass = [5,6,7]

for root, dirs, files in os.walk(CLC_DIR):
    for file in files:
        grass_per = 0
        grass_km2 = 0
        tree_per = 0
        tree_km2 = 0
        tree_fake_per = 0
        tree_fake_km2 = 0
        building_per = 0
        building_km2 = 0
        all_cov = 0
        with rasterio.open(os.path.join(root, file)) as src:
            data = src.read(1)
            tree_cov = np.sum([np.sum(data == x) for x in trees])
            building_cov = np.sum([np.sum(data == x) for x in building])
            grass_cov = np.sum([np.sum(data == x) for x in grass])
            all_cov = np.sum(data != 255)

            grass_per = grass_cov/all_cov
            grass_km = grass_cov*RASTER

            building_per = building_cov/all_cov
            building_km2 = building_cov*RASTER

            tree_fake_per = tree_cov/all_cov
            tree_fake_km2 = tree_cov*RASTER

        with rasterio.open(os.path.join(TREE_DIR, file)) as src:
            data = src.read(1)
            tree_cov = np.sum((data != 240)*(data/100))
            tree_per = tree_cov/all_cov
            tree_km2 = tree_cov*RASTER

        print(file)
        print("Grass_per: ", grass_per)
        print("Tree_per: ", tree_fake_per)
        print("Tree_precise_per: ", tree_per)
        print("Builiding_per: ", building_per)        

        output_J = {
            'grass_per' : float(grass_per),
            'grass_km2' : int(grass_km2),
            'tree_per' : float(tree_fake_per),
            'tree_km2' : int(tree_fake_km2),
            'tree_precise_per' : float(tree_per),
            'tree_precise_km2' : int(tree_km2),
            'building_per' : float(building_per),
            'building_km2' : int(building_km2)
        }

        with open(f"results/{file.split('.')[0]}.json", "w") as f:
            json.dump(output_J, f)            
