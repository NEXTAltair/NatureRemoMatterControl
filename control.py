import asyncio
from kasa import Discover

import subprocess
import logging
import traceback
import time

def control_plug(on_of: bool, ip_address: str, retries: int = 3, delay: int = 5):
    """
    スマートプラグを制御します（再試行機能付き）。
    """
    try:
        for attempt in range(retries):
            try:
                command = ["kasa", "--host", ip_address, "on" if on_of else "off"]
                subprocess.run(command, check=True)
                logging.info(f"プラグを{'オン' if on_of else 'オフ'}にしました。")
                return
            except subprocess.CalledProcessError as e:
                logging.error(f"試行{attempt + 1}でエラーが発生しました: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        raise Exception("プラグの制御に失敗しました。")
    except Exception as e:
        logging.error("Exception occurred in control_plug", exc_info=True)
        traceback.print_exc()
        raise

async def login_tplinknbu():
    dev = await Discover.discover_single("192.168.11.24", username="un@example.com", password="pw")
    await dev.turn_on()
    await dev.update()

if __name__ == "__main__":
    asyncio.run(main())