# Nature Remo API and TP-Link Smart Plug Control

This project demonstrates how to use the Nature Remo API to measure the power consumption of your entire home and control TP-Link smart plugs using the Matter protocol.

## Project Description

The project involves the following components:
- Nature Remo API: Used to gather data from ECHONET Lite devices.
- TP-Link Smart Plugs: Controlled using the Matter protocol.
- Automation Rules: Developed to control devices based on the data collected.
- Dashboard: Created to manage and monitor the smart home devices.

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. Install the required libraries:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your Nature Remo API access token:
   - Obtain your access token from the Nature Remo developer portal.
   - Set the access token in the `monitoring.py` file.

4. Set up your TP-Link Smart Plug:
   - Ensure your TP-Link Smart Plug is connected to your LAN.
   - Follow the instructions in the `control.py` file to configure the smart plug.

## Usage Instructions

### Controlling TP-Link Smart Plugs

To control TP-Link smart plugs using the Matter protocol, follow these steps:

1. Import the necessary functions from the `control.py` file.
2. Use the provided functions to turn on/off the smart plugs based on your requirements.

Example:
```python
from control import turn_on_smart_plug, turn_off_smart_plug

# Turn on the smart plug
turn_on_smart_plug('smart_plug_id')

# Turn off the smart plug
turn_off_smart_plug('smart_plug_id')
```

### Retrieving Data from Nature Remo E

To retrieve data from Nature Remo E, follow these steps:

1. Import the necessary functions from the `monitoring.py` file.
2. Use the provided functions to retrieve and display the data.

Example:
```python
from monitoring import get_nature_remo_data, display_data

# Retrieve data from Nature Remo E
data = get_nature_remo_data()

# Display the retrieved data
display_data(data)
```

The example code provided in the repository demonstrates this process. The code is located in the `1.APIで取得できるプロパティを確認する` section. It sets the access token, sends a GET request to the API endpoint, and prints the JSON response. The response includes details about appliances such as smart meters and electric water heaters, along with their properties and updated values.

For more details, refer to the code in the `1.APIで取得できるプロパティを確認する` section.
