import requests
from datetime import datetime, timedelta
from flight_data import FlightData
from pprint import pprint

TEQUILA_ENDPOINT = "http://tequila-api.kiwi.com"
API_KEY = "267r9VHU1xo17J8ozu5GieCnvEP5Oa-w"
HOME_CODE = "DTW"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        pass

    def get_iata(self, city):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey": API_KEY
        }
        query = {
            "term": city,
            "location_types": "city"
        }

        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def get_prices(self, destination_code):
        today = datetime.now()
        date_from = today.strftime("%d/%m/%Y")
        future = datetime.now() + timedelta(days=180)
        date_to = future.strftime(f"%d/%m/%Y")

        headers = {
            "apikey": API_KEY
        }

        params = {
            "fly_from": HOME_CODE,
            "fly_to": destination_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=params
        )

        try:
            # print(response.json())
            data = response.json()["data"][0]
            print(f"{destination_code} {data['price']}")
        except IndexError:
            params["max_stopovers"] = 1
            resp = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=params
            )
            data = response.json()["data"][0]
            pprint(data)
            flight_data = FlightData(
                price=data["price"],
                orig_city=data["route"][0]["cityFrom"],
                orig_airport=data["route"][0]["flyFrom"],
                dest_city=data["route"][1]["cityTo"],
                dest_airport=data["route"][1]["flyTo"],
                dep_date=data["route"][0]["local_departure"].split("T")[0],
                ret_date=data["route"][2]["local_departure"].split("T")[0],
                layovers=1,
                via_city=data["route"][0]["cityTo"]
            )
        else:
            flight_data = FlightData(
                price=data["price"],
                orig_city=data["route"][0]["cityFrom"],
                orig_airport=data["route"][0]["flyFrom"],
                dest_city=data["route"][0]["cityTo"],
                dest_airport=data["route"][0]["flyTo"],
                dep_date=data["route"][0]["local_departure"].split("T")[0],
                ret_date=data["route"][1]["local_departure"].split("T")[0]
            )
        return flight_data

