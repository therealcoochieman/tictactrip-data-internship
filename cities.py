import pandas as pd
import loader


class City:
    def __init__(self, localName, uniqueName, lat, long, pop):
        # Needs to be done! Sometimes names are nan
        self.localName_ = localName.strip() if type(localName) == str else "not provided"
        self.uniqueName_ = uniqueName.strip() if type(uniqueName) == str else "not provided"
        self.latitude_ = loader.parse_num(lat)
        self.longitude_ = loader.parse_num(long)
        self.population_ = loader.parse_num(pop)

    def __str__(self):
        city = ""
        city += f"local name: {self.localName_}\t"
        city += f"unique name: {self.uniqueName_}\t"
        city += f"latitude: {self.latitude_}\t"
        city += f"longitude: {self.longitude_}\t"
        city += f"population: {self.population_}\t"
        return city


def display_cities(cities):
    for key in sorted(cities.keys()):
        print(f"[{int(key)}]. {cities[key].localName_}")


def display_names(names):
    for name in names:
        print(name)


def load_cities(path):
    file = pd.read_csv(path)
    csv_dict = file.set_index('id').to_dict(orient="index")
    cities = {}
    for i in csv_dict.keys():
        city = csv_dict[i]
        cities[i] = City(city['local_name'], city['unique_name'], city['latitude'], city['longitude'],
                         city['population'])
    return cities
