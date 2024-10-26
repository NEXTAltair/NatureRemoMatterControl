import configparser
from monitoring import get_nature_remo_data, get_instant_power, is_reverse_power_flow
from control import control_plug, login_tplinknbu
from logging_config import setup_logging
import logging
import traceback
import asyncio

class LANError(Exception):
    pass

class InternetError(Exception):
    pass

class NatureAPIError(Exception):
    pass

class TPLinkError(Exception):
    pass

async def main():
    setup_logging()
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['NatureRemo']['token']
    root_ip = config['TPLink']['root_ip']
    device_ips = config['TPLink']['device_ip'].split(',')
    user_name = config['TPLink']['user_name']
    password = config['TPLink']['password']

    for device_ip in device_ips:
        ip_address = f"{root_ip.rsplit('.', 1)[0]}.{device_ip}"

        try:
            dev = await login_tplinknbu(ip_address, user_name, password)
            if dev:
                logging.debug("ログイン成功")
            else:
                raise TPLinkError("ログイン失敗")
        except TPLinkError as e:
            logging.error("TPLinkエラーが発生しました", exc_info=True)
            traceback.print_exc()
            continue
        except Exception as e:
            logging.error("TPLinkログイン中に予期しないエラーが発生しました", exc_info=True)
            traceback.print_exc()
            continue

        while True:
            try:
                logging.info("メインループの反復を開始します")
                appliances = get_nature_remo_data(token)
                data = get_instant_power(appliances)
                reverse_power_flag = is_reverse_power_flow(data[0]['value'])
                await control_plug(dev, reverse_power_flag, ip_address)
                logging.info("メインループの反復が完了しました")
            except NatureAPIError as e:
                logging.error("NatureAPIエラーが発生しました", exc_info=True)
                traceback.print_exc()
            except LANError as e:
                logging.error("LANエラーが発生しました", exc_info=True)
                traceback.print_exc()
            except InternetError as e:
                logging.error("インターネットエラーが発生しました", exc_info=True)
                traceback.print.exc()
            except TPLinkError as e:
                logging.error("TPLinkエラーが発生しました", exc_info=True)
                traceback.print.exc()
            except Exception as e:
                logging.error("予期しないエラーが発生しました", exc_info=True)
                traceback.print.exc()
            await asyncio.sleep(600)  # 次の反復の前に 600 秒待機します

if __name__ == "__main__":
    asyncio.run(main())
