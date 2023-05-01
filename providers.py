import pandas as pd
from enum import Enum
import math

import loader


class TransType(Enum):
    BUS = 1,
    TRAIN = 2,
    CARPOOLING = 3
    CAR = 4

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name


class Provider:
    def __init__(self, company, provider, name, fullname, wifi, plug, adjustable_seats, bicycle, transport_type):
        self.company_ = loader.parse_num(company)
        self.provider_ = provider if type(provider) == str else "not provided"
        self.name_ = name.strip()
        self.fullName_ = fullname.strip()
        self.has_wifi = bool(wifi) if type(wifi) == bool else None
        self.has_plugs = bool(plug) if type(plug) == bool else None
        self.has_adjustable_seats = bool(adjustable_seats) if type(adjustable_seats) == bool else None
        self.has_bicycle = bool(bicycle) if type(adjustable_seats) == bool else None
        self.type = TransType[transport_type.upper()]

    def __str__(self):
        return f"{self.fullName_} ({self.type.name}): {self.name_}\n" \
               f"Company: {self.company_}, Provider: {self.provider_}\n" \
               f"Features: WiFi: {self.has_wifi}, Plugs: {self.has_plugs}, " \
               f"Adjustable seats: {self.has_adjustable_seats}, Bicycle: {self.has_bicycle}"


def load_providers(path):
    file = pd.read_csv(path)
    csv_dict = file.set_index('id').to_dict(orient="index")
    providers = {}
    for i in csv_dict.keys():
        provider = csv_dict[i]
        providers[i] = Provider(provider['company_id'], provider['provider_id'], provider['name'], provider['fullname'],
                                provider['has_wifi'], provider['has_plug'], provider['has_adjustable_seats'],
                                provider['has_bicycle'], provider['transport_type'])
    return providers
