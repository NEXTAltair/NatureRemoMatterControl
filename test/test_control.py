import pytest
from unittest.mock import AsyncMock, patch
from kasa import SmartPlug, Discover
from kasa.exceptions import KasaException
from NatureRemoMatterControl.control_python_kasa.control import control_plug, login_tplinknbu
from NatureRemoMatterControl.exceptions import TPLinkError

@pytest.mark.asyncio
async def test_control_plug_turn_on():
    dev = AsyncMock(spec=SmartPlug)
    await control_plug(dev, True)
    dev.turn_on.assert_called_once()
    dev.update.assert_called()

@pytest.mark.asyncio
async def test_control_plug_turn_off():
    dev = AsyncMock(spec=SmartPlug)
    await control_plug(dev, False)
    dev.turn_off.assert_called_once()
    dev.update.assert_called()

@pytest.mark.asyncio
async def test_control_plug_exception():
    dev = AsyncMock(spec=SmartPlug)
    dev.turn_on.side_effect = KasaException("Error")
    with pytest.raises(TPLinkError, match="スマートプラグの制御に失敗しました。"):
        await control_plug(dev, True)

@pytest.mark.asyncio
@patch('NatureRemoMatterControl.control_python_kasa.control.Discover.discover_single', new_callable=AsyncMock)
async def test_login_tplinknbu_success(mock_discover_single):
    mock_device = AsyncMock(spec=SmartPlug)
    mock_discover_single.return_value = mock_device
    ip_address = "192.168.1.1"
    user_name = "user"
    password = "pass"
    dev = await login_tplinknbu(ip_address, user_name, password)
    mock_discover_single.assert_called_once_with(ip_address, username=user_name, password=password)
    mock_device.update.assert_called_once()
    assert dev == mock_device

@pytest.mark.asyncio
@patch('NatureRemoMatterControl.control_python_kasa.control.Discover.discover_single', new_callable=AsyncMock)
async def test_login_tplinknbu_exception(mock_discover_single):
    mock_discover_single.side_effect = KasaException("Error")
    ip_address = "192.168.1.1"
    user_name = "user"
    password = "pass"
    with pytest.raises(TPLinkError, match="TPLinkアカウントへのログインに失敗しました。"):
        await login_tplinknbu(ip_address, user_name, password)