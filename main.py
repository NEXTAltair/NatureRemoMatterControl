import time
import configparser
from monitoring import get_nature_remo_data, is_reverse_power_flow,get_instant_power
from control import control_plug
from logging_config import setup_logging
import logging
import traceback

def main():
    """
    概要:
        Nature RemoとTP-Linkを使用してスマートホームデバイスを制御するメイン関数。
    詳細:
        この関数は以下のステップを実行します:
        1. ロギングの設定。
        2. 'config.ini'ファイルから設定を読み取る。
        3. 設定からNature Remo APIトークンとTP-LinkデバイスのIPアドレスを取得する。
        4. 無限ループに入り、以下を実行する:
            a. メインループの開始をログに記録。
            b. Nature Remoからデータを取得。
            c. 取得したデータから瞬時電力データを抽出。
            d. 逆潮流があるかどうかを判断。
            e. 逆潮流の状態に基づいてTP-Linkプラグを制御。
            f. メインループの完了をログに記録。
            g. 次の反復の前に1800秒待機。
        5. ループ中に発生した例外をキャッチしてログに記録。
    注意:
        ループは30分の遅延で無期限に実行されます。
    Main function to control the smart home devices using Nature Remo and TP-Link.
    This function performs the following steps:
    1. Sets up logging.
    2. Reads configuration from 'config.ini' file.
    3. Retrieves the Nature Remo API token and TP-Link device IP address from the configuration.
    4. Enters an infinite loop where it:
        a. Logs the start of the main loop iteration.
        b. Fetches data from Nature Remo.
        c. Extracts instant power data from the fetched data.
        d. Determines if there is a reverse power flow.
        e. Controls TP-Link plugs based on the reverse power flow status.
        f. Logs the completion of the main loop iteration.
        g. Waits for 1800 seconds before the next iteration.
    5. Catches and logs any exceptions that occur during the loop.
    Note:
        The loop runs indefinitely with a 30-minute delay between iterations.
    """
    setup_logging()
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['NatureRemo']['token']
    ip_address = config['TPLink']['ip_address']

    while True:
        try:
            logging.info("Starting main loop iteration")
            appliances = get_nature_remo_data(token)
            data = get_instant_power(appliances)
            reverse_power_flag = is_reverse_power_flow(data[0]['value'])
            control_plug(reverse_power_flag, ip_address)
            logging.info("Main loop iteration completed")
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            traceback.print_exc()
        time.sleep(1800)  # # 次の反復の前に 1800 秒待機します /Wait for 1800 seconds before the next iteration

if __name__ == "__main__":
    main()
