import pytest
import requests
from unittest.mock import patch, MagicMock
from nature_remo_con.monitoring.nature_api import (
    get_nature_remo_data,
    get_instant_power,
    is_reverse_power_flow,
    NetworkError
)

# Mock API response from Nature Remo E
mock_api_response_content = {
    "appliances": [
        {
            "nickname": "スマートメーター",
            "type": "EL_SMART_METER",
            "properties": [
                {"epc": "E7", "val": "000001f4", "updated_at": "2024-04-22T08:32:04Z"}
            ],
        }
    ]
}


@patch("nature_remo_con.monitoring.nature_api.requests.get")
def test_get_nature_remo_data_success(mock_get):
    mock_response_json = {"appliances": [{"name": "Light", "id": "123"}]}
    mock_get.return_value = MagicMock()
    mock_get.return_value.json.return_value = mock_response_json
    mock_get.return_value.raise_for_status.return_value = None
    token = "dummy_token"

    data = get_nature_remo_data(token)
    assert data == mock_response_json["appliances"]
    mock_get.assert_called_once_with("https://api.nature.global/1/echonetlite/appliances", headers={"Authorization": f"Bearer {token}"})

@patch("nature_remo_con.monitoring.nature_api.requests.get")
def test_get_nature_remo_data_empty_appliances(mock_get):
    mock_response_json = {"appliances": []}
    mock_get.return_value = MagicMock()
    mock_get.return_value.json.return_value = mock_response_json
    mock_get.return_value.raise_for_status.return_value = None
    token = "dummy_token"

    data = get_nature_remo_data(token)
    assert data == []

@patch("nature_remo_con.monitoring.nature_api.requests.get")
@patch("nature_remo_con.monitoring.nature_api.logger.error")
def test_get_nature_remo_data_http_error(mock_logger_error, mock_get):
    mock_get.return_value = MagicMock()
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API HTTP Error")
    token = "dummy_token"

    with pytest.raises(requests.exceptions.HTTPError):
        get_nature_remo_data(token)
    mock_logger_error.assert_called_once_with("Nature Remo APIでHTTPエラーが発生しました。")

@patch("nature_remo_con.monitoring.nature_api.requests.get")
@patch("nature_remo_con.monitoring.nature_api.logger.error")
def test_get_nature_remo_data_request_exception(mock_logger_error, mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API Network Error")
    token = "dummy_token"

    with pytest.raises(NetworkError) as exc_info:
        get_nature_remo_data(token)
    assert "インターネット接続に問題があります。" in str(exc_info.value)
    mock_logger_error.assert_called_once_with("Nature Remo APIで不明なエラーが発生しました。")


# ECHONETLiteProperty.toml の内容をモックするためのフィクスチャ
@pytest.fixture
def mock_echonetlite_property_toml(monkeypatch):
    mock_data = {
        "EPC": {
            "0x02": {
                "0x88": {
                    "0xE7": {
                        "description": "瞬時電力計測値",
                        "data_type": "signed long",
                        "unit": "W"
                    }
                }
            }
        }
    }
    mock_toml_load = MagicMock(return_value=mock_data)
    monkeypatch.setattr("toml.load", mock_toml_load)
    mock_open = MagicMock()
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_toml_load, mock_open

def test_get_instant_power(mock_echonetlite_property_toml):
    _, mock_open = mock_echonetlite_property_toml
    data = get_instant_power(mock_api_response_content["appliances"])
    assert len(data) == 1
    assert data[0]["appliance_name"] == "スマートメーター"
    assert data[0]["description"] == "瞬時電力計測値"
    assert data[0]["value"] == 500
    assert data[0]["unit"] == "W"
    assert data[0]["updated_at"] == "2024年04月22日 17:32:04"
    mock_open.assert_called_once_with("ECHONETLiteProperty.toml", "r", encoding="utf-8")


def test_is_reverse_power_flow():
    assert is_reverse_power_flow(-100) is True
    assert is_reverse_power_flow(100) is False
    assert is_reverse_power_flow(0) is False
