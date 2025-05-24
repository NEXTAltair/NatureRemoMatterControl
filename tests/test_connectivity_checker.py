# test/test_connectivity_checker.py
import pytest
from unittest.mock import patch, MagicMock
import netifaces
import requests
import socket

from nature_remo_con.connectivity_checker import (
    get_default_gateway,
    ping,
    check_router,
    check_device,
    check_internet_connectivity,
    perform_connectivity_checks,
    RouterUnreachableError,
    DeviceUnreachableError,
    InternetConnectionError,
    ConnectionTimeoutError
)

def test_get_default_gateway():
    with patch('netifaces.gateways') as mock_gateways:
        mock_gateways.return_value = {
            'default': {netifaces.AF_INET: ('192.168.1.1', 'eth0')}
        }
        assert get_default_gateway() == '192.168.1.1'

        mock_gateways.return_value = {}
        assert get_default_gateway() is None

def test_ping_success():
    with patch('socket.create_connection') as mock_create_connection:
        mock_create_connection.return_value = MagicMock()
        assert ping('192.168.1.1') is True

def test_ping_timeout():
    with patch('socket.create_connection', side_effect=socket.timeout):
        with pytest.raises(ConnectionTimeoutError) as exc_info:
            ping('192.168.1.1')
        assert "192.168.1.1 への接続が 2.0 秒でタイムアウトしました。" in str(exc_info.value)

def test_ping_failure():
    """
    Test that ping returns False when a general socket error occurs.
    """
    with patch('socket.create_connection', side_effect=socket.error):
        assert ping('192.168.1.1') is False

def test_check_router_success():
    with patch('nature_remo_con.connectivity_checker.ping', return_value=True) as mock_ping:
        check_router('192.168.1.1')
        mock_ping.assert_called_once_with('192.168.1.1', port=80, timeout=2.0)

def test_check_router_failure():
    with patch('nature_remo_con.connectivity_checker.ping', return_value=False) as mock_ping:
        with pytest.raises(RouterUnreachableError) as exc_info:
            check_router('192.168.1.1')
        assert "192.168.1.1 に到達できません。" in str(exc_info.value)
        mock_ping.assert_called_once_with('192.168.1.1', port=80, timeout=2.0)

def test_check_router_no_gateway():
    with pytest.raises(RouterUnreachableError) as exc_info:
        check_router(None)
    assert "デフォルトゲートウェイが見つかりません。" in str(exc_info.value)

def test_check_device_success():
    with patch('nature_remo_con.connectivity_checker.ping', return_value=True) as mock_ping:
        check_device('192.168.1.2')
        mock_ping.assert_called_once_with('192.168.1.2', port=80, timeout=2.0)

def test_check_device_failure():
    with patch('nature_remo_con.connectivity_checker.ping', return_value=False) as mock_ping:
        with pytest.raises(DeviceUnreachableError) as exc_info:
            check_device('192.168.1.2')
        assert "指定されたIPアドレス 192.168.1.2 に接続できません。" in str(exc_info.value)
        mock_ping.assert_called_once_with('192.168.1.2', port=80, timeout=2.0)

def test_check_internet_connectivity_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        # Expect no exception
        check_internet_connectivity()

def test_check_internet_connectivity_failure_status_code():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        with pytest.raises(InternetConnectionError) as exc_info:
            check_internet_connectivity()
        assert "URL https://www.google.com へのアクセスに失敗しました。ステータスコード: 404" in str(exc_info.value)

def test_check_internet_connectivity_failure_exception():
    with patch('requests.get', side_effect=requests.RequestException("Connection error")):
        with pytest.raises(InternetConnectionError) as exc_info:
            check_internet_connectivity()
        assert "インターネット接続に失敗しました。エラー: Connection error" in str(exc_info.value)

def test_perform_connectivity_checks_success():
    with patch('nature_remo_con.connectivity_checker.get_default_gateway', return_value='192.168.1.1') as mock_get_gw:
        with patch('nature_remo_con.connectivity_checker.check_router') as mock_check_router:
            with patch('nature_remo_con.connectivity_checker.check_device') as mock_check_device:
                with patch('nature_remo_con.connectivity_checker.check_internet_connectivity') as mock_check_internet:
                    with patch('builtins.print') as mock_print:
                        perform_connectivity_checks('192.168.1.2')
                        mock_get_gw.assert_called_once()
                        mock_check_router.assert_called_once_with('192.168.1.1')
                        mock_check_device.assert_called_once_with('192.168.1.2')
                        mock_check_internet.assert_called_once_with("https://www.google.com")
                        mock_print.assert_called_once_with("全ての接続チェックが成功しました。")

def test_perform_connectivity_checks_failure():
    with patch('nature_remo_con.connectivity_checker.get_default_gateway', return_value='192.168.1.1') as mock_get_gw:
        with patch('nature_remo_con.connectivity_checker.check_router') as mock_check_router:
            with patch('nature_remo_con.connectivity_checker.check_device', side_effect=DeviceUnreachableError('192.168.1.2')) as mock_check_device:
                with pytest.raises(DeviceUnreachableError) as exc_info:
                    perform_connectivity_checks('192.168.1.2')
                assert "指定されたIPアドレス 192.168.1.2 に接続できません。" in str(exc_info.value)
                mock_get_gw.assert_called_once()
                mock_check_router.assert_called_once_with('192.168.1.1')
                mock_check_device.assert_called_once_with('192.168.1.2')
