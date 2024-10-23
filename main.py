import time
from monitoring import get_nature_remo_data, display_data
from control import control_plugs_based_on_data

def main():
    token = 'YOUR_ACCESS_TOKEN'
    ip_address = 'YOUR_SMART_PLUG_IP_ADDRESS'
    
    while True:
        data = get_nature_remo_data(token)
        display_data(data)
        control_plugs_based_on_data(data, ip_address)
        time.sleep(60)  # Wait for 60 seconds before the next iteration

if __name__ == "__main__":
    main()
