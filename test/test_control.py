import unittest
from unittest.mock import patch, MagicMock
from control import control_smart_plug, control_plugs_based_on_data

class TestControl(unittest.TestCase):

    @patch('control.SmartPlug')
    def test_control_smart_plug_on(self, MockSmartPlug):
        mock_plug = MockSmartPlug.return_value
        control_smart_plug('192.168.1.100', 'on')
        mock_plug.turn_on.assert_called_once()

    @patch('control.SmartPlug')
    def test_control_smart_plug_off(self, MockSmartPlug):
        mock_plug = MockSmartPlug.return_value
        control_smart_plug('192.168.1.100', 'off')
        mock_plug.turn_off.assert_called_once()

    @patch('control.SmartPlug')
    def test_control_plugs_based_on_data(self, MockSmartPlug):
        mock_plug = MockSmartPlug.return_value
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
        mock_plug.turn_off.assert_called_once()

        data['appliances'][0]['properties'][0]['val'] = '000003e7'  # 999 in hex
        control_plugs_based_on_data(data, '192.168.1.100')
        mock_plug.turn_on.assert_called_once()

if __name__ == '__main__':
    unittest.main()
