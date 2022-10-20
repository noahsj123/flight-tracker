import requests
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

data_manager = DataManager()
sheet_data = data_manager.get_data()
pprint(sheet_data)

flight_search = FlightSearch()

if sheet_data[0]['iataCode'] == "":
    for row in sheet_data:
        row['iataCode'] = flight_search.get_iata(row['city'])
    # print(f"sheet_data:\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_iatas()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

for dest_code in destinations:
    flight = flight_search.get_prices(dest_code["iataCode"])
    ################
    if flight is None:
        continue
    ################


    if flight.price < destinations[dest_code]["price"]:
        message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}" \
                  f"-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, " \
                  f"from {flight.out_date} to {flight.return_date}."

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        if flight.layovers > 0:
            message += f"\nFlight has {flight.layovers}  layover, via {flight.via_city}."
            notification_manager = NotificationManager
            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        notification_manager.send_emails(emails, message, link)



