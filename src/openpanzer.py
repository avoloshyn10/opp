import os, json

countryNames = [
    "All Countries",
    "Slovakia",
    "Belgium",
    "Bulgaria",
    "Czechoslovakia",
    "Denmark",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "USA",
    "Hungary",
    "Turkey",
    "Italy",
    "Netherlands",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Croatia",
    "Russia",
    "Sweden",
    "Allied Yugoslavia",
    "United Kingdom",
    "Yugoslavia",
    "Nationalist Spain",
    "Republican Spain",
]

unitClassNames = [
    "No Class", "Infantry", "Tank", "Recon", "Anti Tank", "Flak", "Fortification",
    "Ground Transport", "Artillery", "Air Defence", "Fighter Aircraft", "Tactical Bomber",
    "Level Bomber", "Air Transport", "Submarine", "Destroyer", "Battleship",
    "Aircraft Carrier", "Naval Transport", "Battle Cruiser", "Cruiser", "Light Cruiser"
]


class Unit:
    def __init__(self, id, name, country, unitClass):
        self.id = id
        self.name = name
        self.country = country
        self.unitClass = unitClass

    def getCountryName(self):
        return countryNames[self.country]

    def getClassName(self):
        return unitClassNames[self.unitClass]

    def getFullName(self):
        return self.getCountryName() + " " + self.name + " " + self.getClassName()


class Equipment:
    def __init__(self, equipmentFolder = "../openpanzer-resources/equipment" ):
        self.eq = {}
        self.equipmentFolder = equipmentFolder

    def loadCountry(self, id):
        name = countryNames[id]
        jsonFile = os.path.join(self.equipmentFolder, "equipment-country-" + str(id) + ".json")

        print "Loading %s for country %s (%d)" % (jsonFile, name, id)
        with open(jsonFile) as jsonData:
            j = json.load(jsonData)
            self.eq.update(self.__unitConverter(j))

    def loadAllCountries(self):
        for id, name in enumerate(countryNames):
            self.loadCountry(id)

    def getUnit(self, id):
        try:
            return self.eq[id]
        except:
            return None

    def __unitConverter(self, json):
        unitsDict = {}
        for u in json["units"]:
            try:
                id = int(u)
                d = json["units"][u]
                unitsDict[id] = Unit(id, d[21], d[22], d[8])
            except:
                pass
        return unitsDict