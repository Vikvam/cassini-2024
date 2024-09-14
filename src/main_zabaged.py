from osgeo import ogr
import json

if __name__ == "__main__":
    FILE = "ZABAGED_RESULTS.gpkg"

    gdb = ogr.Open(FILE)
    layers = [gdb.GetLayerByIndex(i) for i in range(gdb.GetLayerCount())]
    for idx, layer in enumerate(layers):
        name = layer.GetName()
        print(idx, name)
        if idx != 166:
            continue
        area = 0
        for feature in layer:
            print(feature.ExportToJson())
            geom = feature.GetGeometryRef()
            if geom is not None:
                area += geom.GetArea()
                # geom_type = geom.GetGeometryType()
                # print(ogr.GeometryTypeToName(geom_type), geom.GetArea())
        print(area)
