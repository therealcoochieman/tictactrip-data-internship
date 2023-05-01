import pandas as pd
from datetime import datetime, timedelta
import loader

format = '%Y-%m-%d %H:%M:%S+00'

searchFormat = '%Y-%m-%d %H:%M:%S'


def dt_parse(t):
    ret = datetime.strptime(t[0:18], searchFormat)
    if t[19] == '+':
        ret -= timedelta(hours=int(t[20:21]), minutes=int(t[21:]))
    elif t[19] == '-':
        ret += timedelta(hours=int(t[20:21]), minutes=int(t[21:]))
    return ret


class Ticket:
    def __init__(self, company, o_station, d_station, departure_ts, arrival_ts, price_in_cents, search_ts,
                 middle_stations, other_companies, o_city, d_city):
        self.company_ = loader.parse_num(company)
        self.o_station = loader.parse_num(o_station)
        self.d_station = loader.parse_num(d_station)
        self.departure_ts = datetime.strptime(departure_ts, format)
        self.arrival_ts = datetime.strptime(arrival_ts, format)
        self.price_in_cents = loader.parse_num(price_in_cents)
        self.search_ts = dt_parse(search_ts)
        self.middle_stations = middle_stations.strip('}{').split(', ') if type(middle_stations) == str else []
        self.other_companies = other_companies.strip('}{').split(', ') if type(other_companies) == str else []
        self.origin = loader.parse_num(o_city)
        self.dest = loader.parse_num(d_city)

    def __str__(self):
        return f"{self.company_} train from {self.o_station} to {self.d_station}\n" \
               f"Departure: {self.departure_ts}, Arrival: {self.arrival_ts}\n" \
               f"Price: {self.price_in_cents} cents, Search timestamp: {self.search_ts}\n" \
               f"Middle stations: {', '.join(self.middle_stations)}, Other companies: {', '.join(self.other_companies)}\n" \
               f"Origin city: {self.origin}, Destination city: {self.dest}"


def load_tickets(path):
    file = pd.read_csv(path)
    csv_dict = file.set_index('id').to_dict(orient="index")
    tickets = {}
    for i in csv_dict.keys():
        ticket = csv_dict[i]
        tickets[i] = Ticket(ticket["company"], ticket["o_station"], ticket["d_station"], ticket["departure_ts"],
                            ticket["arrival_ts"], ticket["price_in_cents"], ticket["search_ts"],
                            ticket["middle_stations"],
                            ticket["other_companies"], ticket["o_city"], ticket["d_city"])
    return tickets
