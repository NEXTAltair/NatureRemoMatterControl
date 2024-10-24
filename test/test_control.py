import unittest
from unittest.mock import patch, MagicMock
from control import control_smart_plug, control_plugs_based_on_data

class TestControl(unittest.TestCase):

    @patch('control.subprocess.run')
    def test_control_smart_plug_on(self, mock_run):
        control_smart_plug('192.168.1.100', 'on')
        mock_run.assert_called_once_with(["kasa", "--host", '192.168.1.100', "on"], check=True)

    @patch('control.subprocess.run')
    def test_control_smart_plug_off(self, mock_run):
        control_smart_plug('192.168.1.100', 'off')
        mock_run.assert_called_once_with(["kasa", "--host", '192.168.1.100', "off"], check=True)

    @patch('control.subprocess.run')
    def test_control_plugs_based_on_data(self, mock_run):
        data = {
            'appliances': [
                {
                    'properties': [
                        {'epc': 'e7', 'val': '000003e8'}  # 1000 in hex
                    ]
                }
            ]
        }
        control_plugs_based_on_data(data, '192.168.1.100')
        mock_run.assert_called_once_with(["kasa", "--host", '192.168.1.100', "off"], check=True)

        data['appliances'][0]['properties'][0]['val'] = '000003e7'  # 999 in hex
        control_plugs_based_on_data(data, '192.168.1.100')
        mock_run.assert_called_with(["kasa", "--host", '192.168.1.100', "on"], check=True)

if __name__ == '__main__':
    unittest.main()
