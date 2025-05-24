import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from kasa import SmartPlug, SmartDevice
from kasa.exceptions import KasaException
from nature_remo_con.control.python_kasa import (
    control_plug,
    login_tplinknbu,
)
from nature_remo_con.exceptions import TPLinkError


@pytest.mark.asyncio
async def test_control_plug_turn_on():
    dev_mock = AsyncMock(spec=SmartDevice)
    with patch("nature_remo_con.control.python_kasa.logger.info") as mock_logger_info:
        await control_plug(dev_mock, True)
        dev_mock.turn_on.assert_called_once()
        dev_mock.update.assert_called()
        mock_logger_info.assert_called_once_with("プラグをONにしました。")


@pytest.mark.asyncio
async def test_control_plug_turn_off():
    dev_mock = AsyncMock(spec=SmartDevice)
    with patch("nature_remo_con.control.python_kasa.logger.info") as mock_logger_info:
        await control_plug(dev_mock, False)
        dev_mock.turn_off.assert_called_once()
        dev_mock.update.assert_called()
        mock_logger_info.assert_called_once_with("プラグをOFFにしました。")


@pytest.mark.asyncio
async def test_control_plug_exception():
    dev_mock = AsyncMock(spec=SmartDevice)
    dev_mock.turn_on.side_effect = KasaException("Error")
    with patch("nature_remo_con.control.python_kasa.logger.error") as mock_logger_error:
        with pytest.raises(TPLinkError, match="スマートプラグの制御に失敗しました。"):
            await control_plug(dev_mock, True)
        mock_logger_error.assert_called_once_with("Exception occurred in control_plug")


@pytest.mark.asyncio
@patch("nature_remo_con.control.python_kasa.Discover.discover_single", new_callable=AsyncMock)
@patch("nature_remo_con.control.python_kasa.logger.debug")
async def test_login_tplinknbu_success(mock_logger_debug, mock_discover_single):
    mock_device = AsyncMock(spec=SmartDevice)
    mock_discover_single.return_value = mock_device
    ip_address = "192.168.1.1"
    user_name = "user"
    password = "pass"
    dev = await login_tplinknbu(ip_address, user_name, password)
    mock_discover_single.assert_called_once_with(
        ip_address, username=user_name, password=password
    )
    mock_device.update.assert_called_once()
    assert dev == mock_device
    mock_logger_debug.assert_called_once_with("Login successful")


@pytest.mark.asyncio
@patch("nature_remo_con.control.python_kasa.Discover.discover_single", new_callable=AsyncMock)
@patch("nature_remo_con.control.python_kasa.logger.error")
async def test_login_tplinknbu_device_not_found(mock_logger_error, mock_discover_single):
    mock_discover_single.return_value = None
    ip_address = "192.168.1.99"
    user_name = "user"
    password = "pass"
    dev = await login_tplinknbu(ip_address, user_name, password)
    assert dev is None
    mock_logger_error.assert_called_once_with(f"デバイス {ip_address} が見つかりませんでした。")


@pytest.mark.asyncio
@patch("nature_remo_con.control.python_kasa.Discover.discover_single", new_callable=AsyncMock)
@patch("nature_remo_con.control.python_kasa.logger.error")
async def test_login_tplinknbu_exception(mock_logger_error, mock_discover_single):
    mock_discover_single.side_effect = KasaException("Error")
    ip_address = "192.168.1.1"
    user_name = "user"
    password = "pass"
    with pytest.raises(
        TPLinkError, match="TPLinkアカウントへのログインに失敗しました。"
    ):
        await login_tplinknbu(ip_address, user_name, password)
    mock_logger_error.assert_called_once_with("Login failed")
