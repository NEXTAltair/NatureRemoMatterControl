import requests
from tplink_smartplug import SmartPlug
import logging
import traceback

# Function to control TP-Link smart plugs using Matter protocol
# Matterプロトコルを利用してTP-Linkスマートプラグを制御する機能
def control_smart_plug(ip_address, state):
    try:
        logging.info("Starting control_smart_plug function")
        plug = SmartPlug(ip_address)
        if state == "on":
            plug.turn_on()
        elif state == "off":
            plug.turn_off()
        else:
            print("Invalid state. Use 'on' or 'off'.")
        logging.info("Completed control_smart_plug function")
    except Exception as e:
        logging.error("Exception occurred in control_smart_plug", exc_info=True)
        traceback.print_exc()
        raise

# Function to turn on/off smart plugs based on data from Nature Remo E
# Nature Remo EのデータをもとにスマートプラグをON/OFFする機能
def control_plugs_based_on_data(data, ip_address):
    try:
        logging.info("Starting control_plugs_based_on_data function")
        for appliance in data['appliances']:
            for prop in appliance['properties']:
                if prop['epc'] == 'e7':  # Example EPC code for power consumption
                    power_consumption = int(prop['val'], 16)
                    if power_consumption > 1000:  # Example threshold value
                        control_smart_plug(ip_address, "off")
                    else:
                        control_smart_plug(ip_address, "on")
        logging.info("Completed control_plugs_based_on_data function")
    except Exception as e:
        logging.error("Exception occurred in control_plugs_based_on_data", exc_info=True)
        traceback.print_exc()
        raise
