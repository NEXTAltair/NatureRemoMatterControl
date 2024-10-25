import pytest
import requests
from unittest.mock import patch
from monitoring import get_nature_remo_data, get_instant_power, is_reverse_power_flow

# Mock API response from Nature Remo E
mock_response = {
    'appliances': [
        {
            'nickname': 'スマートメーター',
            'type': 'EL_SMART_METER',
            'properties': [
                {'epc': 'E7', 'val': '000001d8', 'updated_at': '2024-04-22T08:32:04Z'}
            ]
        }
    ]
}

# Nature Remo APIからのレスポンスをモックするテストケース
@patch('monitoring.requests.get')
def test_get_nature_remo_data(mock_get):
    # 正常なモックレスポンス
    mock_response = {'appliances': [{'name': 'Light', 'id': '123'}]}
    mock_get.return_value.json.return_value = mock_response
    token = 'dummy_token'

    # 正常系テスト
    data = get_nature_remo_data(token)
    assert data == mock_response['appliances']

    # 空リストのケースをテスト
    mock_get.return_value.json.return_value = {'appliances': []}
    data = get_nature_remo_data(token)
    assert data == []

    # エラー時のケースをテスト
    mock_get.side_effect = requests.RequestException("API Error")
    data = get_nature_remo_data(token)
    assert data == []  # エラー時は空リストが返ることを確認


# Test case to verify data parsing and display
def test_get_instant_power():
    data = get_instant_power(mock_response['appliances'])
    assert len(data) == 1
    assert data[0]['appliance_name'] == 'スマートメーター'
    assert data[0]['description'] == '瞬時電力計測値'
    assert data[0]['value'] == 472
    assert data[0]['unit'] == 'W'
    assert data[0]['updated_at'] == '2024年04月22日 17:32:04'

# Test case to verify reverse power flow detection
def test_is_reverse_power_flow():
    assert is_reverse_power_flow(-100) == True
    assert is_reverse_power_flow(100) == False
