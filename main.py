import time
import configparser
from monitoring import get_nature_remo_data, display_data
from control import control_plugs_based_on_data

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['NatureRemo']['token']
    ip_address = config['TPLink']['ip_address']
    
    while True:
        data = get_nature_remo_data(token)
        display_data(data)
        control_plugs_based_on_data(data, ip_address)
        time.sleep(60)  # Wait for 60 seconds before the next iteration

if __name__ == "__main__":
    main()
