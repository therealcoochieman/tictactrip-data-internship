import math

import cities
import loader
import providers
import stations
import ticket_data
from providers import TransType
from datetime import timedelta
from geopy.distance import geodesic
from unidecode import unidecode

cities_dict = cities.load_cities("../Resources/cities.csv")
ordered_cities = {}
providers_dict = providers.load_providers("../Resources/providers.csv")
stations_dict = stations.load_stations("../Resources/stations.csv")
tickets = ticket_data.load_tickets("../Resources/ticket_data.csv")
average_info = {}


def route_price():
    # origin & dest -> find all matching ones in tickets
    # cost
    matchings = {}
    for _, ticket in tickets.items():
        matchings.setdefault((ticket.origin, ticket.dest), []).append(ticket.price_in_cents / 100)

    # find min, max and average
    for key, route in matchings.items():
        trip = 'from ' + cities_dict[key[0]].uniqueName_ + ' to ' + cities_dict[key[1]].uniqueName_ + ':'
        print(trip)
        print("\tminimal price = " + str(min(route)) + " euros")
        print("\taverage price = " + str(sum(route) / len(route)) + " euros")
        print("\tmaximal price = " + str(max(route)) + " euros")


def route_duration():
    # origin & dest -> find all matching ones in tickets
    # time = end - start timestamp
    matchings = {}
    for _, ticket in tickets.items():
        matchings.setdefault((ticket.origin, ticket.dest), []).append(
            (ticket.arrival_ts.timestamp() - ticket.departure_ts.timestamp()))

    # find min, max and average
    for key, route in matchings.items():
        trip = 'from ' + cities_dict[key[0]].uniqueName_ + ' to ' + cities_dict[key[1]].uniqueName_ + ':'
        print(trip)
        print("\tminimal duration = " + str(timedelta(seconds=min(route))) + " hours")
        print("\taverage duration = " + str(timedelta(seconds=sum(route) / len(route))) + " hours")
        print("\tmaximal duration = " + str(timedelta(seconds=max(route))) + " hours")


def specific_route_duration():
    origin = select_country("Please input the ID of your origin city.")
    dest = select_country("Please input the ID of your destination city.")
    if origin == dest:
        print("Honestly it should not take more than 20 minutes, you're already there!")
    # filters from all tickets only the ones with the correct origin/destination
    # I could have made it bidirectional (origin accepted as destination, destination as origin...)
    filtered = filter(lambda dict_ticket: dict_ticket[1].dest == dest and dict_ticket[1].origin == origin,
                      tickets.items())
    time = []
    for _, ticket in filtered:
        time.append(ticket.arrival_ts.timestamp() - ticket.departure_ts.timestamp())
    if len(time) == 0:
        print(
            f"There are currently no information about any trips from {cities_dict[origin].localName_} to "
            + f"{cities_dict[dest].localName_}, sorry!")
    else:
        print(
            f"On average, a trip from {cities_dict[origin].localName_} to {cities_dict[dest].localName_} "
            + f"takes {timedelta(seconds=sum(time) / len(time))}")


def place_value_in_range(distance):
    if distance <= 200:
        return 200
    elif distance <= 800:
        return 800
    elif distance <= 2000:
        return 2000
    else:
        return math.inf


# not sure why I made it its own function, only 1 usage!
# I love iterables
def filter_by_transport_mode(ticket_list, mode):
    return list(filter(lambda ticket: providers_dict[ticket.company_].type == mode, ticket_list))


def compute_time_and_price_average(ticket_list, mode):
    filtered = filter_by_transport_mode(ticket_list, mode)
    time = 0
    price = 0
    for ticket in filtered:
        time += ticket.arrival_ts.timestamp() - ticket.departure_ts.timestamp()
        price += ticket.price_in_cents / 100

    # not pretty but avoids division by 0! :D
    return time / len(filtered) if len(filtered) != 0 else 0, price / len(filtered) if len(filtered) != 0 else None


# creates a dict taking as key intervals of distance (200, 800, 2000, math.inf) and as value ticket items
def compute_route_ranges():
    routes = {}
    for _, route in tickets.items():
        # get position (latitude, longitude) for both origin & destination
        origin = (cities_dict[route.origin].latitude_, cities_dict[route.origin].longitude_)
        destination = (cities_dict[route.dest].latitude_, cities_dict[route.dest].longitude_)
        distance = geodesic(origin, destination).km
        routes.setdefault(place_value_in_range(distance), []).append(route)
    return routes


def compute_average_info():
    route_ranges = compute_route_ranges()
    for key in sorted(route_ranges.keys()):
        for mode in TransType:
            time, price = compute_time_and_price_average(route_ranges[key], mode)
            average_info[(key, mode)] = (time, price)


def get_average_info():
    if len(average_info) == 0:
        compute_average_info()
    return average_info


# creates a dict taking as key a country, as value another dict which itself takes as key a region and as value city IDs
# computed based on city.localName_
def order_cities():
    for key, city in cities_dict.items():
        city_info = city.localName_.split(',')
        if len(city_info) > 1 and not any(len(elm) == 0 for elm in city_info):
            ordered_cities.setdefault(unidecode(city_info[-1].strip()), {}).setdefault(unidecode(city_info[-2].strip()),
                                                                                       []).append(key)


def get_order_cities():
    if len(ordered_cities) == 0:
        order_cities()
    return ordered_cities


def display_route_ranges():
    route_ranges = get_average_info()
    i = 0
    for key in sorted(route_ranges.keys()):
        # that's janky but the only way I found to make it pretty...
        if i % 4 == 0:
            print(f"Averages for range < {key[0]}")
        time, price = route_ranges[key]
        mode = key[1]
        i += 1
        if time == 0 and not price:
            print(f"\tNo data for {mode} transportation mode")
        else:
            print(
                f"\ttime & price for {mode} transportation mode: {str(timedelta(seconds=time))} hours, {price} euros")


def select_city(city_list, string):
    city = -1
    while city not in city_list:
        for c in city_list:
            print(f"[{int(c)}]. {cities_dict[c].localName_}")
        city = loader.input_num(string)

    return city


def select_region(country, string):
    region = ""
    ordered = get_order_cities()
    while region not in ordered[country].keys():
        cities.display_names(ordered[country].keys())
        region = input(f"Input a region of {country} displayed above")

    return select_city(ordered[country][region], string)


def select_country(string):
    ordered = get_order_cities()
    country = ""
    while country not in ordered.keys():
        cities.display_names(ordered.keys())
        country = input("Input a country displayed above.")

    return select_region(country, string)


# Returns a list of all tickets going from a designated origin to a designated destination (User Input)
def select_route():
    origin = select_country("Please enter the ID of the origin city.")
    dest = select_country("Please enter the ID of the destination city.")
    return origin, dest, list(
        filter(lambda ticket: ticket[1].origin == origin and ticket[1].dest == dest, tickets.items()))


def select_transport_mode():
    types = [mode.name for mode in TransType]
    while True:
        mode = input("Choose between bus, car, carpooling, train.")
        if mode.upper() in types:
            # the fact that this works? I love Python
            return TransType.__members__[mode.upper()]


def predict_origin_to_dest():
    origin, dest, routes = select_route()
    if origin == dest:
        print("You are already at your destination! You silly goose")
        return
    origin = cities_dict[origin]
    dest = cities_dict[dest]
    distance = geodesic((origin.latitude_, origin.longitude_), (dest.latitude_, dest.longitude_)).km
    mode = select_transport_mode()
    route_ranges = get_average_info()
    time, price = route_ranges[(place_value_in_range(distance), mode)]
    if time == 0 or not price:
        print("Sadly, there are not enough information. I am a machine, not a guru!")
    else:
        print(
            f"On average, a trip from {origin.localName_} to {dest.localName_} " +
            f" would cost around {price} euros and take {timedelta(seconds=time)} hours.")
