from osgeo import ogr

if __name__ == "__main__":
    FILE = "ZABAGED_RESULTS.gpkg"

    gdb = ogr.Open(FILE)
    layers = [gdb.GetLayerByIndex(i) for i in range(gdb.GetLayerCount())]
    layer = gdb.GetLayerByIndex(166)
    for feature in layer:
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryType() == 6:
            for i in range(geometry.GetGeometryCount()):  # Iterate over rings
                ring = geometry.GetGeometryRef(i)
                print(ring)
                print(ring.GetPointCount())
                for j in range(ring.GetPointCount()):
                    x, y, _ = ring.GetPoint(j)  # Get coordinates
                    print(f"Polygon Point Coordinates: ({x}, {y})")
