import requests
import logging
import traceback

# Function to retrieve data from Nature Remo E using API
# APIを利用してNature Remo Eからデータを取得する機能
def get_nature_remo_data(token):
    try:
        logging.info("Starting get_nature_remo_data function")
        url = "https://api.nature.global/1/echonetlite/appliances"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers)
        logging.info("Completed get_nature_remo_data function")
        return response.json()
    except Exception as e:
        logging.error("Exception occurred in get_nature_remo_data", exc_info=True)
        traceback.print_exc()
        raise

# Function to parse and display JSON response
# JSONレスポンスを解析して表示する関数
def display_data(data):
    try:
        logging.info("Starting display_data function")
        for appliance in data['appliances']:
            print(f"Appliance: {appliance['nickname']}")
            for prop in appliance['properties']:
                print(f"  EPC: {prop['epc']}, Value: {prop['val']}, Updated at: {prop['updated_at']}")
        logging.info("Completed display_data function")
    except Exception as e:
        logging.error("Exception occurred in display_data", exc_info=True)
        traceback.print_exc()
        raise
