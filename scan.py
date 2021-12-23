import datetime

example_url = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1043241/sgtf_regionepicurve_2021-12-21.csv"


def create_url(asset_number):
    # Create a URL using yesterday's date
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    url = f"https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/{asset_number}/sgtf_regionepicurve_{yesterday_str}.csv"
    return url


import requests
import sys

last_asset_file = open("last_asset_number.txt", "rt")

starting_asset_number = int(last_asset_file.read())
number_to_try = 500


def scan():
    for asset_number in range(starting_asset_number,
                              starting_asset_number + number_to_try):
        url = create_url(asset_number)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return url, asset_number
            else:
                print(f"Was not at {asset_number}")
        except requests.exceptions.RequestException as e:
            print(f"Exception for {asset_number}")
    return None, None


correct_url, asset_number = scan()

if asset_number:
    print(f"Found at {asset_number}")
    with open("last_asset_number.txt", "wt") as f:
        f.write(str(asset_number))

if correct_url:
    print(f"Found at {correct_url}")
    # Download to file
    response = requests.get(correct_url)
    content = response.content

    if b"Signon" not in content:
        with open("sgtf_regionepicurve.csv", "wb") as f:
            f.write(content)
        # also save to dated_file
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        with open(f"sgtf_regionepicurve_{yesterday_str}.csv", "wb") as f:
            f.write(content)
    else:
        print("File is currently private")
else:
    print("Not found")
