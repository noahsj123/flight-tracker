import requests
from pprint import pprint

SHEETY_ENDPOINT = "https://api.sheety.co/8caaf70da57086cf9b62b4497fff7dfe/copyOfFlightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        print (self.destination_data)
        # print(result)
        return self.destination_data

    def update_iatas(self):
        for city in self.destination_data:
            new_data = {
                "price" : {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

