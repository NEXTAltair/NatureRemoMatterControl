import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from main import main

@pytest.fixture
def config_mock():
    config = MagicMock()
    config['NatureRemo']['token'] = 'fake_token'
    config['TPLink']['ip_address'] = '192.168.1.1'
    config['TPLink']['user_name'] = 'admin'
    config['TPLink']['password'] = 'password'
    return config

@pytest.fixture
def nature_remo_data_mock():
    return MagicMock(return_value=[{'value': 100}])

@pytest.fixture
def instant_power_mock():
    return MagicMock(return_value=[{'value': 100}])

@pytest.fixture
def reverse_power_flow_mock():
    return False

@pytest.fixture
def tplink_device_mock():
    return AsyncMock()

@pytest.fixture
def setup_logging_mock():
    return MagicMock()

@pytest.fixture
def control_plug_mock():
    return AsyncMock()

@pytest.fixture
def login_tplinknbu_mock():
    return MagicMock()

@pytest.mark.asyncio
async def test_main(config_mock, nature_remo_data_mock, instant_power_mock, reverse_power_flow_mock,
                   tplink_device_mock, setup_logging_mock, control_plug_mock,
                   login_tplinknbu_mock):
    with patch('main.asyncio.sleep', return_value=None), \
         patch('main.login_tplinknbu', return_value=login_tplinknbu_mock), \
         patch('main.setup_logging', return_value=setup_logging_mock), \
         patch('main.control_plug', return_value=control_plug_mock), \
         patch('main.configparser.ConfigParser', return_value=config_mock), \
         patch('main.get_nature_remo_data', return_value=nature_remo_data_mock()), \
         patch('main.get_instant_power', return_value=instant_power_mock()), \
         patch('main.is_reverse_power_flow', return_value=reverse_power_flow_mock):

        task = asyncio.create_task(main())
        await asyncio.sleep(0.1)  # メインループを一度実行
        task.cancel()

        setup_logging_mock.assert_called_once()
        login_tplinknbu_mock.assert_called_once_with('192.168.1.1', 'admin', 'password')
        nature_remo_data_mock.assert_called_once_with('fake_token')
        instant_power_mock.assert_called_once_with(nature_remo_data_mock())
        control_plug_mock.assert_called_once_with(tplink_device_mock(), False, '192.168.1.1')