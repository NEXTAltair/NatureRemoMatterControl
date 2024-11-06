import logging
import traceback
from kasa import Discover
from ..exceptions import TPLinkError


async def control_plug(dev, on_of: bool):
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
        logging.info(f"プラグを{on_off_str}にしました。")
        return
    except Exception as e:
        logging.error("Exception occurred in control_plug", exc_info=True)
        traceback.print_exc()
        raise TPLinkError("スマートプラグの制御に失敗しました。") from e


async def login_tplinknbu(ip_address: str, user_name: str, password: str):
    try:
        dev = await Discover.discover_single(
            ip_address, username=user_name, password=password
        )
        await dev.update()
        logging.debug("Login successful")
        return dev
    except Exception as e:
        logging.error("Login failed", exc_info=True)
        traceback.print_exc()
        raise TPLinkError("TPLinkアカウントへのログインに失敗しました。") from e
