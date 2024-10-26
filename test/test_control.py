import unittest
from unittest.mock import patch, MagicMock
from control import login_tplinknbu, control_plug
from main import LANError, InternetError, NatureAPIError, TPLinkError

class TestControl(unittest.TestCase):

    @patch('control.Discover.discover_single')
    async def test_login_tplinknbu(self, mock_discover_single):
        mock_device = MagicMock()
        mock_discover_single.return_value = mock_device

        ip_address = '192.168.1.100'
        user_name = 'test_user'
        password = 'test_password'

        result = await login_tplinknbu(ip_address, user_name, password)

        mock_discover_single.assert_called_once_with(ip_address, username=user_name, password=password)
        mock_device.turn_on.assert_called_once()
        mock_device.update.assert_called_once()
        self.assertTrue(result)

    @patch('control.control_plug')
    async def test_control_plug_lan_error(self, mock_control_plug):
        mock_control_plug.side_effect = LANError("LAN connection error occurred")
        dev = MagicMock()
        ip_address = '192.168.1.100'
        with self.assertRaises(LANError):
            await control_plug(dev, True, ip_address)

    @patch('control.control_plug')
    async def test_control_plug_internet_error(self, mock_control_plug):
        mock_control_plug.side_effect = InternetError("Internet connection timeout occurred")
        dev = MagicMock()
        ip_address = '192.168.1.100'
        with self.assertRaises(InternetError):
            await control_plug(dev, True, ip_address)

    @patch('control.control_plug')
    async def test_control_plug_nature_api_error(self, mock_control_plug):
        mock_control_plug.side_effect = NatureAPIError("Nature Remo API error occurred")
        dev = MagicMock()
        ip_address = '192.168.1.100'
        with self.assertRaises(NatureAPIError):
            await control_plug(dev, True, ip_address)

    @patch('control.control_plug')
    async def test_control_plug_tplink_error(self, mock_control_plug):
        mock_control_plug.side_effect = TPLinkError("TPLink error occurred")
        dev = MagicMock()
        ip_address = '192.168.1.100'
        with self.assertRaises(TPLinkError):
            await control_plug(dev, True, ip_address)

if __name__ == '__main__':
    unittest.main()
