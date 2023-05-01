import pandas as pd

import loader

class Station:
    def __init__(self, unique_name,lat,long):
        self.unique_name_ = unique_name.strip()
        self.latitude_ = loader.parse_num(lat)
        self.longitude_ = loader.parse_num(long)

    def __str__(self):
        return f"{self.unique_name_} (latitude: {self.latitude_}, longitude: {self.longitude_})"


def load_stations(path):
    file = pd.read_csv(path)
    csv_dict = file.set_index('id').to_dict(orient="index")
    stations = {}
    for i in csv_dict.keys():
        station = csv_dict[i]
        stations[i] = Station(station["unique_name"], station["latitude"], station["longitude"])
    return stations


load_stations("Resources/stations.csv")