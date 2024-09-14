import csv

CADASTRE_DATA = "../dataset/UHDP.csv"


class PotentialCalculator:
    def __init__(self):
        csvfile = open(CADASTRE_DATA)
        self.reader = csv.reader(csvfile)

    def potential_coverage(self, parcel_number: int):
        """
        Returns: tuple(max sidliste, max korunni)
        Sidliste: les+trava+voda+chmelnice+vinice
        Korunni: les+trava

        If the parcel_number is not found, return None
        """
        BEER_ROW = 5
        VINE_ROW = 6
        GARDEN_ROW = 7
        GRASS_ROW = 9
        FOREST_ROW = 10
        WATER_ROW = 11
        OTHER_ROW = 13

        found = None
        for i, r in enumerate(self.reader):
            if i != 0 :
                if int(r[0]) == parcel_number:
                    found = r
                    break

        if found == None:
            return None

        # check just to be sure (the OSTATNI row should be the last)
        if OTHER_ROW > len(found):
            return None

        forest = int(found[FOREST_ROW-1])
        grass = int(found[GRASS_ROW-1])
        garden = int(found[GARDEN_ROW-1])
        water = int(found[WATER_ROW-1])
        beer = int(found[BEER_ROW-1])
        vine = int(found[VINE_ROW-1])
        other = int(found[OTHER_ROW-1])

        korunni = forest + grass + garden
        sidliste = korunni + water + beer + vine + other

        return (korunni, sidliste)


