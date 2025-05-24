import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from nature_remo_con.main import main, handle_device
from nature_remo_con.logging_config import setup_logging
from loguru import logger

@pytest.fixture
def config_mock():
    config = MagicMock()
    config["TPLink"] = {"device_ip": "100"}
    return config

@pytest.fixture
def nature_remo_data_mock_content():
    return [{'updated_at': '2023-01-01T00:00:00Z', 'description': 'power', 'value': 100, 'unit': 'W'}]

@pytest.fixture
def mock_logger_setup(monkeypatch):
    mock_logger = MagicMock()
    monkeypatch.setattr(logger, 'debug', mock_logger.debug)
    monkeypatch.setattr(logger, 'info', mock_logger.info)
    monkeypatch.setattr(logger, 'warning', mock_logger.warning)
    monkeypatch.setattr(logger, 'error', mock_logger.error)
    original_setup_logging = setup_logging
    def mock_setup_logging_wrapper():
        logger_instance = original_setup_logging()
        mock_setup_logging_wrapper.called = True
        return logger_instance
    mock_setup_logging_wrapper.called = False
    monkeypatch.setattr('nature_remo_con.main.setup_logging', mock_setup_logging_wrapper)
    return mock_setup_logging_wrapper, mock_logger

@pytest.mark.asyncio
async def test_main_loop_logic(mock_logger_setup, nature_remo_data_mock_content, monkeypatch, config_mock):
    monkeypatch.setenv("NATURE_REMO_TOKEN", "fake_token")
    monkeypatch.setenv("TPLINK_USERNAME", "admin")
    monkeypatch.setenv("TPLINK_PASSWORD", "password")

    mock_setup_logging, mock_log_methods = mock_logger_setup

    mock_handle_device = AsyncMock(side_effect=asyncio.CancelledError)
    monkeypatch.setattr('nature_remo_con.main.handle_device', mock_handle_device)

    mock_config_parser_instance = config_mock
    mock_config_parser_instance["TPLink"] = {"device_ip": "100"}
    mock_config_parser_class = MagicMock(return_value=mock_config_parser_instance)
    monkeypatch.setattr('nature_remo_con.main.configparser.ConfigParser', mock_config_parser_class)
    monkeypatch.setenv("DEFAULT_GATEWAY", "192.168.1.1")

    with pytest.raises(asyncio.CancelledError):
        await main()

    assert mock_setup_logging.called
    mock_handle_device.assert_called_once_with("192.168.1.100", "admin", "password", "fake_token")