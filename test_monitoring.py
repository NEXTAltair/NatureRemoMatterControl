import pytest
from unittest.mock import patch
from monitoring import get_nature_remo_data, display_data

# Mock API response from Nature Remo E
mock_response = {
    'appliances': [
        {
            'nickname': 'Smart Meter',
            'properties': [
                {'epc': 'e7', 'val': '000001d8', 'updated_at': '2024-04-22T08:32:04Z'}
            ]
        }
    ]
}

# Test case to mock API responses from Nature Remo E
@patch('monitoring.requests.get')
def test_get_nature_remo_data(mock_get):
    mock_get.return_value.json.return_value = mock_response
    token = 'dummy_token'
    data = get_nature_remo_data(token)
    assert data == mock_response

# Test case to verify data parsing and display
def test_display_data(capsys):
    display_data(mock_response)
    captured = capsys.readouterr()
    assert "Appliance: Smart Meter" in captured.out
    assert "EPC: e7, Value: 000001d8, Updated at: 2024-04-22T08:32:04Z" in captured.out
