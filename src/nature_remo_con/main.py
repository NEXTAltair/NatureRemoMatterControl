import asyncio
import logging
import traceback
import os

from pathlib import Path
import configparser
from dotenv import load_dotenv
from .monitoring.nature_api import (
    get_nature_remo_data,
    get_instant_power,
    is_reverse_power_flow,
)
from .control.python_kasa import (
    control_plug,
    login_tplinknbu,
)
from .logging_config import setup_logging
from .exceptions import NetworkError, TPLinkError


async def handle_device(ip_address: str, user_name: str, password: str, token: str):
    try:
        dev = await login_tplinknbu(ip_address, user_name, password)
    except TPLinkError:
        logging.error("TPLinkエラーが発生しました", exc_info=True)
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
        except TPLinkError:
            logging.error("TPLinkエラーが発生しました", exc_info=True)
            traceback.print_exc()
        except Exception:
            logging.error("予期しないエラーが発生しました", exc_info=True)
            traceback.print_exc()
        await asyncio.sleep(
            600
        )  # 次の反復の前に 600 秒待機します /Wait for 600 seconds before the next iteration


async def main():
    load_dotenv()
    setup_logging()
    config = configparser.ConfigParser()
    # スクリプトファイルの絶対パスを取得し、そこからプロジェクトルートを特定
    # main.py -> nature_remo_con -> src -> project_root
    project_root_dir = Path(__file__).resolve().parent.parent.parent
    config_file_path = project_root_dir / "config" / "config.ini"
    
    # エンコーディングを指定して読み込み
    config.read(config_file_path, encoding='utf-8')
    # 機密情報は環境変数から取得
    token = os.getenv("NATURE_REMO_TOKEN")
    root_ip = os.getenv("DEFAULT_GATEWAY")
    device_ips = config["TPLink"]["device_ip"].split(",")
    user_name = os.getenv("TPLINK_USERNAME")
    password = os.getenv("TPLINK_PASSWORD")

    tasks = []
    for device_ip in device_ips:
        ip_address = f"{root_ip.rsplit('.', 1)[0]}.{device_ip}"
        task = asyncio.create_task(
            handle_device(ip_address, user_name, password, token)
        )
        tasks.append(task)

    await asyncio.gather(*tasks)


def cli():
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
