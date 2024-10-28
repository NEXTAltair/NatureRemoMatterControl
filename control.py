from kasa import Discover
import logging
import traceback

async def control_plug(dev: Discover, on_of: bool):
    """
    スマートプラグを制御
    """
    try:
        if on_of:
            await dev.turn_on()
            await dev.update()
        else:
            await dev.turn_off()
            await dev.update()
        logging.info(f"プラグを{on_of}にしました。")
        return
    except Exception as e:
        logging.error(f"Exception occurred in control_plug{e}", exc_info=True)
        traceback.print_exc()
        raise

async def login_tplinknbu(ip_address: str, user_name: str, password: str):
    try:
        dev = await Discover.discover_single(ip_address, username=user_name, password=password)
        await dev.update()
        logging.debug("Login successful")
        return dev
    except Exception as e:
        logging.error(f"Login failed{e}", exc_info=True)
        traceback.print_exc()
        return False