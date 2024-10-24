import logging
import requests
import toml
from datetime import datetime, timezone, timedelta

# Nature Remo APIからデータを取得する関数
def get_nature_remo_data(token):
    url = "https://api.nature.global/1/echonetlite/appliances"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('appliances', [])

# EPCコードをフォーマットする関数
def format_epc(epc):
    return '0x' + epc.upper() if isinstance(epc, str) else '0x{:02X}'.format(epc)

# スマートメーターの瞬時電力計測値を取得する関数
def get_instant_power(appliances):
    with open('ECHONETLiteProperty.toml', 'r', encoding='utf-8') as file:
        epc_definitions = toml.load(file)

    result = []
    for appliance in appliances:
        name = appliance['nickname']
        appliance_type = appliance.get('type', '')
        if name != 'スマートメーター' or appliance_type != 'EL_SMART_METER':
            continue  # スマートメーター以外はスキップ

        properties = appliance.get('properties', [])
        for prop in properties:
            epc = format_epc(prop.get('epc'))
            value = prop.get('val')
            updated_at = prop.get('updated_at')

            if epc != '0xE7':
                continue  # 瞬時電力計測値以外はスキップ

            epc_info = epc_definitions.get('EPC', {}).get('0x02', {}).get('0x88', {}).get(epc)
            if not epc_info:
                continue

            description = epc_info.get('description', 'Unknown')
            data_type = epc_info.get('data_type', 'Unknown')
            unit = epc_info.get('unit', 'W')

            try:
                parsed_value = int(value, 16)
                if data_type.startswith('signed'):
                    bit_length = len(value) * 4
                    if parsed_value >= 2 ** (bit_length - 1):
                        parsed_value -= 2 ** bit_length
            except ValueError:
                parsed_value = value

            # 日付を日本時間に変換
            updated_at_dt = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')
            updated_at_dt = updated_at_dt.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=9)))
            updated_at_str = updated_at_dt.strftime('%Y年%m月%d日 %H:%M:%S')

            result.append({
                'appliance_name': name,
                'description': description,
                'value': parsed_value,
                'unit': unit,
                'updated_at': updated_at_str
            })

    return result

# データを表示する関数
def display_instant_power(data):
    for item in data:
        negative = is_reverse_power_flow(item['value'])
        print(f"機器名: {item['appliance_name']}")
        print(f"  {item['description']}: {item['value']} {item['unit']} (更新日時: {item['updated_at']})")
        print(f"  逆潮流: {negative}")

# 瞬時電力計測値が負の値かどうかを判定する関数
def is_reverse_power_flow(value: int) -> bool:
    logging.info(f"value: {value}")
    return value < 0

if __name__ == "__main__":
    import configparser

    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        token = config['NatureRemo']['token']

        appliances = get_nature_remo_data(token)
        data = get_instant_power(appliances)
        display_instant_power(data)

    except Exception as e:
        print("エラーが発生しました:", e)
