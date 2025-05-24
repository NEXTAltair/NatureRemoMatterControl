import asyncio
from loguru import logger
import traceback
import os
import sys
from typing import cast

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
        if dev is None:
            logger.error(f"デバイス {ip_address} への接続に失敗しました。")
            return
    except TPLinkError:
        logger.error("TPLinkエラーが発生しました")
        traceback.print_exc()
        return
    except NetworkError as e:
        logger.error(
            f"TPLinkログイン中に予期しないエラーが発生しました: {e}"
        )
        traceback.print_exc()
        return

    previous_reverse_power_flag = None

    while True:
        try:
            logger.debug("メインループの反復を開始します")
            assert dev is not None
            appliances = get_nature_remo_data(token)
            data = get_instant_power(appliances)
            if not data:
                logger.warning("Nature Remoからデータを取得できませんでした。")
                await asyncio.sleep(60)
                continue
            data_dict = data[0]
            logger.info(f"{data_dict['updated_at']})")
            logger.info(
                f"{data_dict['description']}: {data_dict['value']} {data_dict['unit']}"
            )
            reverse_power_flag = is_reverse_power_flow(data_dict["value"])
            if reverse_power_flag != previous_reverse_power_flag:
                await control_plug(dev, reverse_power_flag)
            previous_reverse_power_flag = reverse_power_flag
            logger.debug("メインループの反復が完了しました")
        except NetworkError as e:
            logger.error(f"ネットワークでエラー: {e}")
            traceback.print_exc()
        except TPLinkError:
            logger.error("TPLinkエラーが発生しました")
            traceback.print_exc()
        except IndexError:
            logger.error("取得したデータ形式が正しくありません。")
            traceback.print_exc()
        except Exception:
            logger.error("予期しないエラーが発生しました")
            traceback.print_exc()
        await asyncio.sleep(
            600
        )


async def main():
    load_dotenv()
    setup_logging()
    config = configparser.ConfigParser()
    project_root_dir = Path(__file__).resolve().parent.parent.parent
    config_file_path = project_root_dir / "config" / "config.ini"
    
    config.read(config_file_path, encoding='utf-8')
    
    token_env = os.getenv("NATURE_REMO_TOKEN")
    root_ip_env = os.getenv("DEFAULT_GATEWAY")
    user_name_env = os.getenv("TPLINK_USERNAME")
    password_env = os.getenv("TPLINK_PASSWORD")

    if not all([token_env, root_ip_env, user_name_env, password_env]):
        missing_vars = []
        if not token_env: missing_vars.append("NATURE_REMO_TOKEN")
        if not root_ip_env: missing_vars.append("DEFAULT_GATEWAY")
        if not user_name_env: missing_vars.append("TPLINK_USERNAME")
        if not password_env: missing_vars.append("TPLINK_PASSWORD")
        logger.error(f"必要な環境変数が設定されていません: {', '.join(missing_vars)}")
        sys.exit(1)
    
    token: str = cast(str, token_env)
    root_ip: str = cast(str, root_ip_env)
    user_name: str = cast(str, user_name_env)
    password: str = cast(str, password_env)

    device_ips_str = config["TPLink"]["device_ip"]
    if not device_ips_str:
        logger.error("設定ファイルに device_ip が見つかりません。")
        sys.exit(1)
    device_ips = device_ips_str.split(",")

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
