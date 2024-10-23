import requests

# Function to retrieve data from Nature Remo E using API
def get_nature_remo_data(token):
    url = "https://api.nature.global/1/echonetlite/appliances"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to parse and display JSON response
def display_data(data):
    for appliance in data['appliances']:
        print(f"Appliance: {appliance['nickname']}")
        for prop in appliance['properties']:
            print(f"  EPC: {prop['epc']}, Value: {prop['val']}, Updated at: {prop['updated_at']}")
