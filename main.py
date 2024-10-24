import time
import configparser
from monitoring import get_nature_remo_data, get_instant_power, is_reverse_power_flow
from control import control_plugs_based_on_data, login_tplinknbu
from logging_config import setup_logging
import logging
import traceback
import asyncio

async def main():
    setup_logging()
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['NatureRemo']['token']
    ip_address = config['TPLink']['ip_address']
    user_name = config['TPLink']['user_name']
    password = config['TPLink']['password']

    await login_tplinknbu(ip_address, user_name, password)

    while True:
        try:
            logging.info("Starting main loop iteration")
            appliances = get_nature_remo_data(token)
            data = get_instant_power(appliances)
            reverse_power_flag = is_reverse_power_flow(data[0]['value'])
            await control_plugs_based_on_data(reverse_power_flag, ip_address)
            logging.info("Main loop iteration completed")
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            traceback.print_exc()
        await asyncio.sleep(1800)  # # 次の反復の前に 1800 秒待機します /Wait for 1800 seconds before the next iteration

if __name__ == "__main__":
    asyncio.run(main())
