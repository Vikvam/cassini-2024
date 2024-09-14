import glob

from matplotlib import pyplot as plt
from osgeo import ogr
import json


"""
https://cuzk.gov.cz/Katastr-nemovitosti/Poskytovani-udaju-z-KN/Vymenny-format-KN/Vymenny-format-ISKN-v-textovem-tvaru/Popis_VF_ISKN-v6_1.aspx
BUDOVY_DEF {
    'ID'                ?
    'ID_2'              ?
    'TYPPPD_KOD'        ?
    'KATUZE_KOD'        Katastrální území
    'TEXT_KM'           Číslo popisné
    'SO_KOD'            ?
}
PARCELY_KN_DEF {
    'ID'                ?
    'ID_2'              ?
    'TYPPPD_KOD'        Číselník typů prvků prostorových dat
    'KATUZE_KOD'        ?
    'TEXT_KM'           Číslo parcely
    'PAR_VYMERA'        v m^2
    'DRUPOZ_KOD'        Kód druhu pozemku
    'ZPVYPA_KOD'        Způsob využití nemovitosti
    'BUD_ID'            ?
    'STAV_PARC'         ?
KATASTRALNI_UZEMI_DEF {
    'TYPPPD_KOD'        Číselník typů prvků prostorových dat
    'KOD'               Kód katastrálního území
    'TEXT_KM'           Název katastrálního území
    'ID_2'              ?
    'ID'                ?
"""

# {'ID': '1184', 'ID_2': '2399220604', 'TYPPPD_KOD': '100018', 'KATUZE_KOD': 723754, 'TEXT_KM': '170/1', 'PAR_VYMERA': 8, 'DRUPOZ_KOD': 14, 'ZPVYPA_KOD': 19, 'BUD_ID': None, 'STAV_PARC': 'n'}


def plot_layer(layer, ax):
    name = layer.GetName()
    print(name)
    for idx, feature in enumerate(layer):
        geometry = feature.GetGeometryRef()
        properties = {field: feature.GetField(field) for field in feature.keys()}
        print(properties)
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

    for file in glob.glob("katastr/723754/*_DEF.shp"):
        data = driver.Open(file, 0)
        layer = data.GetLayer()

        extent = layer.GetExtent()

        plot_layer(layer, ax)

        ax.set_xlim(min(ax.get_xlim()[0], extent[0]), max(ax.get_xlim()[1], extent[1]))
        ax.set_ylim(min(ax.get_ylim()[0], extent[2]), max(ax.get_ylim()[1], extent[3]))

    # plt.legend()
    # plt.show()
