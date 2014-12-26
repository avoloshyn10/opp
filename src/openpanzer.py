
equipmentFolder = "../openpanzer-resources/equipment"

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
	"Level Bomber", "Air Transport", "Submarine" , "Destroyer", "Battleship",
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


def unitConverter(json):
	unitsDict = {}
	for u in json["units"]:
		try:
			id = int(u)
			d = json["units"][u]
			unitsDict[id] = Unit(id, d[21], d[22], d[8])
		except:
			pass
	return unitsDict