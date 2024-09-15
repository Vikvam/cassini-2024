import glob

from matplotlib import pyplot as plt
import geopandas as gpd
import json

def get_avail_tree_area(catastr_folder):
    def get_features_dict(gdf, key):
        features = {}
        for idx, row in gdf.iterrows():
            properties = row.drop("geometry").to_dict()
            if key in properties.keys():
                features[properties[key]] = row
        return features

    def get_features(gdf, filter):
        features = []
        for idx, row in gdf.iterrows():
            properties = row.drop("geometry").to_dict()
            filters_ok = True
            for key in filter.keys():
                if key not in properties.keys() or not filter[key](properties[key]):
                    filters_ok = False
            if filters_ok:
                features.append(row)
        return features

    gpd_parcely_def = gpd.read_file(f"{catastr_folder}/PARCELY_KN_DEF.shp")
    gpd_parcely_poly = gpd.read_file(f"{catastr_folder}/PARCELY_KN_P.shp")
    features_parcely_poly = get_features_dict(gpd_parcely_poly, "ID")
    return_arr = [] 

    for feature in get_features(
        gpd_parcely_def, 
        {"DRUPOZ_KOD": lambda property: property == 15 or property == 11}
    ):
        feature_P = features_parcely_poly[feature["ID"]]
        return_arr.append(feature_P[0]["geometry"])

    return return_arr


if __name__ == "__main__":
    print(get_avail_tree_area("727024"))
