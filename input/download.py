import json
import requests
import csv
import datetime
import re
import os
from datetime import datetime, timedelta


def main():
    # Read csv using csv.DictReader
    with open('restaurants.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Get data from website
            data = get_data(row['restaurant_code'])

            pretty_name = row['restaurant_name'].split("-")[0].lower()
            pretty_name = "data/" + re.sub('[^A-Za-z0-9]+', '', pretty_name)

            # If the data obtained from the get_data function is different from the data saved in "{pretty_name}-{get_date(-1)}.json", save the data to a new file
            if not os.path.isfile(f"{pretty_name}-{get_date(-1)}.json") or data != json.load(open(f"{pretty_name}-{get_date(-1)}.json")):
                with open(f"{pretty_name}-{get_date()}.json", 'w') as outfile:
                    json.dump(data, outfile)
            else:
                print(f"{pretty_name}-{get_date(-1)}.json is up to date")
                # rename the file from "{pretty_name}-{get_date(-1)}.json" to "{pretty_name}-{get_date()}.json"
                os.rename(f"{pretty_name}-{get_date(-1)}.json", f"{pretty_name}-{get_date()}.json")


def get_date(offset=0):
    # Get current date in YYYYMMDD format
    date = datetime.now() + timedelta(days=offset)
    return date.strftime("%Y%m%d")


def get_data(restaurant_code, latitude=15, longitude=120):
    # Get json data from website
    url = f"[REDACTED_API_URL]vendors/{restaurant_code}?include=menus,bundles,multiple_discounts&language_id=1&dynamic_pricing=0&opening_type=delivery&basket_currency=PHP&latitude={latitude}&longitude={longitude}"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    main()
