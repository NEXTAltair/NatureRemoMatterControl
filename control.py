import asyncio
from kasa import Discover
import logging
import traceback

def control_plug(on_of: bool, ip_address: str):
    """
    スマートプラグを制御
    """
    try:
        command = ["kasa", "--host", ip_address, on_of]
        subprocess.run(command, check=True)
        logging.info(f"プラグを{on_of}にしました。")
        return
    except Exception as e:
        logging.error("Exception occurred in control_plug", exc_info=True)
        traceback.print_exc()
        raise

async def login_tplinknbu(ip_address: str, user_name: str, password: str):
    dev = await Discover.discover_single(ip_address, username=user_name, password=password)
    await dev.turn_on()
    await dev.update()
