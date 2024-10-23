import requests
from kasa import SmartPlug

# Function to control TP-Link smart plugs using Matter protocol
def control_smart_plug(ip_address, state):
    plug = SmartPlug(ip_address)
    if state == "on":
        plug.turn_on()
    elif state == "off":
        plug.turn_off()
    else:
        print("Invalid state. Use 'on' or 'off'.")

# Function to turn on/off smart plugs based on data from Nature Remo E
def control_plugs_based_on_data(data, ip_address):
    for appliance in data['appliances']:
        for prop in appliance['properties']:
            if prop['epc'] == 'e7':  # Example EPC code for power consumption
                power_consumption = int(prop['val'], 16)
                if power_consumption > 1000:  # Example threshold value
                    control_smart_plug(ip_address, "off")
                else:
                    control_smart_plug(ip_address, "on")
