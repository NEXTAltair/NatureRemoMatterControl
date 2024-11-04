# ディレクトリ構造変更Ver
import configparser
from monitoring.nature_api import (
    get_nature_remo_data,
    get_instant_power,
    is_reverse_power_flow,
)
from control.python_kasa import (
    control_plug,
    login_tplinknbu,
)
from logging_config import setup_logging
from exceptions import NetworkError, TPLinkError

import asyncio
import logging
import traceback


async def handle_device(ip_address: str, user_name: str, password: str, token: str):
    try:
        dev = await login_tplinknbu(ip_address, user_name, password)
    except TPLinkError:
        logging.error(f"TPLinkエラーが発生しました", exc_info=True)
        traceback.print_exc()
        return
    except NetworkError as e:
        logging.error(
            f"TPLinkログイン中に予期しないエラーが発生しました: {e}", exc_info=True
        )
        traceback.print_exc()
        return

    previous_reverse_power_flag = None

    while True:
        try:
            logging.debug("メインループの反復を開始します")
            appliances = get_nature_remo_data(token)
            data = get_instant_power(appliances)
            data_dict = data[0]
            logging.info(f"{data_dict['updated_at']})")
            logging.info(
                f"{data_dict['description']}: {data_dict['value']} {data_dict['unit']}"
            )
            reverse_power_flag = is_reverse_power_flow(data_dict["value"])
            if reverse_power_flag != previous_reverse_power_flag:
                await control_plug(dev, reverse_power_flag)
            previous_reverse_power_flag = reverse_power_flag
            logging.debug("メインループの反復が完了しました")
        except NetworkError as e:
            logging.error(f"ネットワークでエラー: {e}", exc_info=True)
            traceback.print_exc()
        except TPLinkError as e:
            logging.error("TPLinkエラーが発生しました", exc_info=True)
            traceback.print_exc()
        except Exception as e:
            logging.error("予期しないエラーが発生しました", exc_info=True)
            traceback.print_exc()
        await asyncio.sleep(
            600
        )  # 次の反復の前に 600 秒待機します /Wait for 600 seconds before the next iteration


async def main():
    setup_logging()
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    token = config["NatureRemo"]["token"]
    root_ip = config["local"]["root_ip"]
    device_ips = config["TPLink"]["device_ip"].split(",")
    user_name = config["TPLink"]["user_name"]
    password = config["TPLink"]["password"]

    tasks = []
    for device_ip in device_ips:
        ip_address = f"{root_ip.rsplit('.', 1)[0]}.{device_ip}"
        task = asyncio.create_task(
            handle_device(ip_address, user_name, password, token)
        )
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
