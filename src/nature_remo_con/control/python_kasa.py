from loguru import logger
import traceback
from kasa import Discover, SmartDevice
from ..exceptions import TPLinkError
from typing import Optional


async def control_plug(dev: SmartDevice, on_of: bool):
    """
    スマートプラグを制御
    """
    try:
        if on_of:
            on_off_str = "ON"
            await dev.turn_on()
            await dev.update()
        else:
            on_off_str = "OFF"
            await dev.turn_off()
            await dev.update()
        logger.info(f"プラグを{on_off_str}にしました。")
        return
    except Exception as e:
        logger.error("Exception occurred in control_plug")
        traceback.print_exc()
        raise TPLinkError("スマートプラグの制御に失敗しました。") from e


async def login_tplinknbu(ip_address: str, user_name: str, password: str) -> Optional[SmartDevice]:
    try:
        dev = await Discover.discover_single(
            ip_address, username=user_name, password=password
        )
        if dev:
            await dev.update()
            logger.debug("Login successful")
            return dev
        else:
            logger.error(f"デバイス {ip_address} が見つかりませんでした。")
            return None
    except Exception as e:
        logger.error("Login failed")
        traceback.print_exc()
        raise TPLinkError("TPLinkアカウントへのログインに失敗しました。") from e
