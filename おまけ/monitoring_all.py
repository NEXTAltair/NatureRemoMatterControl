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

# プロパティを変換する関数
def convert_properties(appliances):
    with open('ECHONETLiteProperty.toml', 'r', encoding='utf-8') as file:
        epc_definitions = toml.load(file)

    type_to_codes = {
        'EL_SMART_METER': {'group_code': '0x02', 'class_code': '0x88'},
        'EL_ELECTRIC_WATER_HEATER': {'group_code': '0x02', 'class_code': '0x6B'},
    }

    result = []
    for appliance in appliances:
        name = appliance['nickname']
        appliance_type = appliance.get('type', '')
        properties = appliance.get('properties', [])

        type_info = type_to_codes.get(appliance_type, {})
        group_code = type_info.get('group_code', '')
        class_code = type_info.get('class_code', '')

        meter_factors = {}

        for prop in properties:
            epc = format_epc(prop.get('epc'))
            value = prop.get('val')
            updated_at = prop.get('updated_at')

            epc_info = (
                epc_definitions.get('EPC', {}).get('SuperClass', {}).get(epc) or
                epc_definitions.get('EPC', {}).get(group_code, {}).get(class_code, {}).get(epc)
            )

            if not epc_info:
                continue

            description = epc_info.get('description', 'Unknown')
            data_type = epc_info.get('data_type', 'Unknown')
            unit = epc_info.get('unit', '')
            values_mapping = epc_info.get('values', {})

            try:
                if data_type.startswith('unsigned') or data_type.startswith('signed'):
                    parsed_value = int(value, 16)
                    if data_type.startswith('signed'):
                        bit_length = len(value) * 4
                        if parsed_value >= 2 ** (bit_length - 1):
                            parsed_value -= 2 ** bit_length
                else:
                    parsed_value = value
            except ValueError:
                parsed_value = value

            mapped_value = values_mapping.get('0x{:02X}'.format(parsed_value), parsed_value) if isinstance(parsed_value, int) else parsed_value

            if appliance_type == 'EL_SMART_METER':
                if epc == '0xD3':
                    meter_factors['coefficient'] = parsed_value
                elif epc == '0xE1':
                    unit_mapping = {0x00: 1, 0x01: 0.1, 0x02: 0.01, 0x03: 0.001, 0x04: 0.0001,
                                    0x0A: 10, 0x0B: 100, 0x0C: 1000, 0x0D: 10000}
                    meter_factors['unit'] = unit_mapping.get(parsed_value, 1)
                    mapped_value = values_mapping.get('0x{:02X}'.format(parsed_value), parsed_value)

            result.append({
                'appliance_name': name,
                'description': description,
                'value': parsed_value,
                'unit': unit,
                'updated_at': updated_at,
                'epc': epc,
                'mapped_value': mapped_value,
                'appliance_type': appliance_type,
            })

        # スマートメーターの積算電力量を計算
        for data in result:
            if data['appliance_type'] == 'EL_SMART_METER':
                coef = meter_factors.get('coefficient', 1)
                unit_val = meter_factors.get('unit', 1)
                if data['epc'] in ['0xE0', '0xE3']:
                    if isinstance(data['value'], int):
                        data['value'] = data['value'] * coef * unit_val
                        data['unit'] = 'kWh'
                elif data['epc'] == '0xE7':
                    data['unit'] = 'W'

    return result

# データを表示する関数
def display_data(appliances):
    data = convert_properties(appliances)
    appliances_dict = {}
    for item in data:
        name = item['appliance_name']
        appliances_dict.setdefault(name, []).append(item)

    for name, items in appliances_dict.items():
        print(f"機器名: {name}")
        for item in items:
            updated_at = datetime.strptime(item['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
            updated_at = updated_at.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=9)))
            updated_at_str = updated_at.strftime('%Y年%m月%d日 %H:%M:%S')
            value = item['mapped_value'] if item['mapped_value'] != item['value'] else item['value']
            unit = item['unit']
            value_display = f"{value} {unit}".strip()
            print(f"  {item['description']}: {value_display} (更新日時: {updated_at_str})")

if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['NatureRemo']['token']

    appliances = get_nature_remo_data(token)
    display_data(appliances)
