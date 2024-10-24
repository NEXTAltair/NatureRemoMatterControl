import subprocess
import logging
import traceback

def control_plug(on_of: bool, ip_address: str):
    """
    Controls a smart plug using the Kasa command line tool.
    スマートプラグをKasaコマンドラインツールで制御します。

    Parameters:
    on_of (bool): If True, turns the plug on. If False, turns the plug off.
    on_of (bool): Trueの場合、プラグをオンにします。Falseの場合、プラグをオフにします。
    ip_address (str): The IP address of the smart plug.
    ip_address (str): スマートプラグのIPアドレス。

    Raises:
    Exception: If an error occurs while trying to control the smart plug.
    Exception: スマートプラグを制御しようとした際にエラーが発生した場合。
    """
    try:
        if on_of:
            subprocess.run(["kasa", "--host", ip_address, "on"], check=True)
        else:
            subprocess.run(["kasa", "--host", ip_address, "off"], check=True)
    except Exception as e:
        logging.error("Exception occurred in control_smart_plug", exc_info=True)
        traceback.print_exc()
        raise
