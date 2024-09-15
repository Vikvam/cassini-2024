import csv

CADASTRE_DATA = "../dataset/UHDP.csv"


class PotentialCalculator:
    def __init__(self):
        csvfile = open(CADASTRE_DATA, 'r', encoding='windows-1250')
        self.reader = csv.reader(csvfile, delimiter=';')

    def potential_coverage(self, parcel_number: int):
        """
        Returns: tuple(max sidliste, max korunni)
        Sidliste: les+trava+voda+chmelnice+vinice
        Korunni: les+trava

        If the parcel_number is not found, return None
        """
        BEER_ROW = 8
        VINE_ROW = 10
        GARDEN_ROW = 12
        GRASS_ROW = 16
        FOREST_ROW = 18
        WATER_ROW = 20
        OTHER_ROW = 24

        found = None
        for i, r in enumerate(self.reader):
            # skip first line
            if i != 0 :
                if int(r[0]) == parcel_number:
                    found = r
                    break

        if found == None:
            return None

        # check just to be sure (the OSTATNI row should be the last)
        # it loads one extra row, lower by one
        if OTHER_ROW > len(found)-1:
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

