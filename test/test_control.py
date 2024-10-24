import unittest
from unittest.mock import patch, MagicMock
from control import login_tplinknbu

class TestControl(unittest.TestCase):

    @patch('control.Discover.discover_single')
    async def test_login_tplinknbu(self, mock_discover_single):
        mock_device = MagicMock()
        mock_discover_single.return_value = mock_device

        ip_address = '192.168.1.100'
        user_name = 'test_user'
        password = 'test_password'

        await login_tplinknbu(ip_address, user_name, password)

        mock_discover_single.assert_called_once_with(ip_address, username=user_name, password=password)
        mock_device.turn_on.assert_called_once()
        mock_device.update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
