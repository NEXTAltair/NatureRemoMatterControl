import time
import configparser
from monitoring import get_nature_remo_data, display_data
from control import control_plugs_based_on_data
from logging_config import setup_logging
import logging
import traceback

def main():
    setup_logging()
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['NatureRemo']['token']
    ip_address = config['TPLink']['ip_address']

    while True:
        try:
            logging.info("Starting main loop iteration")
            data = get_nature_remo_data(token)
            display_data(data)
            control_plugs_based_on_data(data, ip_address)
            logging.info("Main loop iteration completed")
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            traceback.print_exc()
        time.sleep(60)  # Wait for 60 seconds before the next iteration

if __name__ == "__main__":
    main()
