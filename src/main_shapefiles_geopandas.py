import glob
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


def get_features(gdf, filter: dict):
    features = []
    for idx, row in gdf.iterrows():
        properties = row.drop("geometry").to_dict()
        filters_ok = True
        for key in filter.keys():
            if key not in properties.keys() or properties[key] != filter[key]:
                filters_ok = False
        if filters_ok:
            features.append(row)
    return features


if __name__ == "__main__":
    fig, ax = plt.subplots()

    for file in glob.glob("katastr/723754/*_DEF.shp"):
        gdf = gpd.read_file(file)

        for feature in get_features({"DRUPOZ_KOD": 14}):
            print(feature)

    #     print(file)
    #     plot_layer(gdf, ax)
    #
    #     ax.set_xlim(min(ax.get_xlim()[0], gdf.total_bounds[0]), max(ax.get_xlim()[1], gdf.total_bounds[2]))
    #     ax.set_ylim(min(ax.get_ylim()[0], gdf.total_bounds[1]), max(ax.get_ylim()[1], gdf.total_bounds[3]))
    #
    # plt.legend()
    # plt.show()
