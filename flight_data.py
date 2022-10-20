from datetime import datetime

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, orig_city, orig_airport, dest_city, dest_airport, dep_date, ret_date, layovers=0, via_city=""):
        self.price = price
        self.origin_city = orig_city
        self.origin_airport = orig_airport
        self.destination_city = dest_city
        self.destination_airport = dest_airport
        self.out_date = dep_date
        self.return_date = ret_date
        self.layovers = layovers
        self.via_city = via_city


