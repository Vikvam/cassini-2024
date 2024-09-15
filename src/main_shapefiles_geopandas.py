import glob
from typing import Callable

import geopandas as gpd
import matplotlib.pyplot as plt


def plot_layer(gdf, ax):
    for idx, row in gdf.iterrows():
        geometry = row.geometry
        properties = row.drop("geometry").to_dict()
        print(properties)
        if geometry.geom_type == "Polygon":
            x, y = geometry.exterior.xy
            ax.plot(x, y, "b-", label=row.name if idx == 0 else None)
        elif geometry.geom_type == "Point":
            x, y = geometry.x, geometry.y
            ax.plot(x, y, "ro", label=row.name if idx == 0 else None)


def get_features(gdf, filter: dict[str, Callable]):
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


if __name__ == "__main__":
    fig, ax = plt.subplots()

    BUD_ID = "59946757010"
    PARCEL_ID = "1284"

    gpd_parcely_def = gpd.read_file("katastr/723754/PARCELY_KN_DEF.shp")
    gpd_parcely_p = gpd.read_file("katastr/723754/PARCELY_KN_P.shp")

    # PARCELY DATA:
    # {'ID': '1284', 'ID_2': '88009157010', 'TYPPPD_KOD': '100028', 'KATUZE_KOD': 723754, 'TEXT_KM': '56/11', 'PAR_VYMERA': 28, 'DRUPOZ_KOD': 13, 'ZPVYPA_KOD': None, 'BUD_ID': '59946757010', 'STAV_PARC': 'a'}
    # ID 1284, ID_2 88009157010, TYPPPD_KOD 9100301, KATUZE_KOD 723754, OBEC_KOD 549096

    for feature in get_features(gpd_parcely_def, {"BUD_ID": lambda property: property == "59946757010"}):
        print(feature)
    for feature in get_features(gpd_parcely_p, {"ID": lambda property: property == "1284"}):
        print(feature)


    gpd_budovy_def = gpd.read_file("katastr/723754/BUDOVY_DEF.shp")
    gpd_budovy_p = gpd.read_file("katastr/723754/BUDOVY_P.shp")

    # BUDOVY DATA:
    # {'ID': '197', 'ID_2': '59946757010', 'TYPPPD_KOD': '9100101', 'KATUZE_KOD': 723754, 'TEXT_KM': 'bez čp/če', 'SO_KOD': 107329247}

    for feature in get_features(gpd_budovy_def, {"ID_2": lambda property: property == BUD_ID}):
        print(feature)

    for feature in get_features(gpd_budovy_p, {"ID_2": lambda property: property == BUD_ID}):
        print(feature)
