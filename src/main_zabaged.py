from osgeo import ogr

if __name__ == "__main__":
    FILE = "ZABAGED_RESULTS.gdb"

    gdb = ogr.Open(FILE)
    layers = [gdb.GetLayerByIndex(i) for i in range(gdb.GetLayerCount())]
