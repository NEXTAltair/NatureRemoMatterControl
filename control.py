import requests
from matter import MatterDevice

# Function to control Matter smart plugs
def control_smart_plug(device_id, state):
    device = MatterDevice(device_id)
    if state == "on":
        device.turn_on()
    elif state == "off":
        device.turn_off()
    else:
        print("Invalid state. Use 'on' or 'off'.")

# Function to turn on/off smart plugs based on data from Nature Remo E
def control_plugs_based_on_data(data, device_id):
    for appliance in data['appliances']:
        for prop in appliance['properties']:
            if prop['epc'] == 'e7':  # Example EPC code for power consumption
                power_consumption = int(prop['val'], 16)
                if power_consumption > 1000:  # Example threshold value
                    control_smart_plug(device_id, "off")
                else:
                    control_smart_plug(device_id, "on")
