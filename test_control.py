import unittest
from unittest.mock import patch, MagicMock
from control import control_smart_plug, control_plugs_based_on_data

class TestControl(unittest.TestCase):

    @patch('control.MatterDevice')
    def test_control_smart_plug_on(self, MockMatterDevice):
        mock_device = MockMatterDevice.return_value
        control_smart_plug('matter_device_id', 'on')
        mock_device.turn_on.assert_called_once()

    @patch('control.MatterDevice')
    def test_control_smart_plug_off(self, MockMatterDevice):
        mock_device = MockMatterDevice.return_value
        control_smart_plug('matter_device_id', 'off')
        mock_device.turn_off.assert_called_once()

    @patch('control.MatterDevice')
    def test_control_plugs_based_on_data(self, MockMatterDevice):
        mock_device = MockMatterDevice.return_value
        data = {
            'appliances': [
                {
                    'properties': [
                        {'epc': 'e7', 'val': '000003e8'}  # 1000 in hex
                    ]
                }
            ]
        }
        control_plugs_based_on_data(data, 'matter_device_id')
        mock_device.turn_off.assert_called_once()

        data['appliances'][0]['properties'][0]['val'] = '000003e7'  # 999 in hex
        control_plugs_based_on_data(data, 'matter_device_id')
        mock_device.turn_on.assert_called_once()

if __name__ == '__main__':
    unittest.main()
