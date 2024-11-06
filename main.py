import configparser
from monitoring import get_nature_remo_data, get_instant_power, is_reverse_power_flow
from control import control_plug, login_tplinknbu
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

    dev = await login_tplinknbu(ip_address, user_name, password)
    if dev:
        logging.debug("Login successful")
    else:
        logging.error("Login failed")

    previous_reverse_power_flag = None

    while True:
        try:
            logging.debug("Starting main loop iteration")
            appliances = get_nature_remo_data(token)
            data = get_instant_power(appliances)
            data_dict = data[0]
            logging.info(f"{data_dict['updated_at']} {data_dict['description']}: {data_dict['value']} {data_dict['unit']}")
            reverse_power_flag = is_reverse_power_flow(data_dict['value'])

            if reverse_power_flag != previous_reverse_power_flag:
                await control_plug(dev, reverse_power_flag, ip_address)

            previous_reverse_power_flag = reverse_power_flag
            logging.debug("Main loop iteration completed")
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            traceback.print_exc()
        await asyncio.sleep(1800)  # # 次の反復の前に 1800 秒待機します /Wait for 1800 seconds before the next iteration

if __name__ == "__main__":
    asyncio.run(main())
