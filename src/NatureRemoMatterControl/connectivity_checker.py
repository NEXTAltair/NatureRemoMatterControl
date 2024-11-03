# connectivity_checker.py
import netifaces
import socket
import requests
from typing import Optional
from NatureRemoMatterControl.exceptions import (
    NetworkError,
    RouterUnreachableError,
    DeviceUnreachableError,
    InternetConnectionError,
    ConnectionTimeoutError,
)


def get_default_gateway() -> Optional[str]:
    """デフォルトゲートウェイ（ルーター）のIPアドレスを取得します。"""
    gateways = netifaces.gateways()
    default_gateway = gateways.get("default")
    if default_gateway:
        # IPv4のデフォルトゲートウェイを取得
        return default_gateway.get(netifaces.AF_INET)[0]
    return None


import socket


def ping(host: str, port: int = 80, timeout: float = 2.0) -> bool:
    """
    指定されたホストとポートに対してTCP接続を試み、到達性を確認します。
    成功すればTrueを返し、タイムアウト時にはConnectionTimeoutErrorを投げます。
    その他の失敗時にはFalseを返します。
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except socket.timeout as exc:
        raise ConnectionTimeoutError(host, timeout) from exc
    except socket.error:
        return False


def check_router(router_ip: Optional[str], port: int = 80, timeout: float = 2.0):
    """ルーターへの到達性を確認します。"""
    if not router_ip:
        raise RouterUnreachableError(
            router_ip="デフォルトゲートウェイが見つかりません。"
        )
    if not ping(router_ip, port=port, timeout=timeout):
        raise RouterUnreachableError(router_ip)


def check_device(device_ip: str, port: int = 80, timeout: float = 2.0):
    """指定されたデバイスへの到達性を確認します。"""
    if not ping(device_ip, port=port, timeout=timeout):
        raise DeviceUnreachableError(device_ip)


def check_internet_connectivity(
    test_url: str = "https://www.google.com", timeout: float = 5.0
):
    """インターネット接続を確認します。"""
    try:
        response = requests.get(test_url, timeout=timeout)
        if response.status_code != 200:
            raise InternetConnectionError(
                f"URL {test_url} へのアクセスに失敗しました。ステータスコード: {response.status_code}"
            )
    except requests.RequestException as e:
        raise InternetConnectionError(
            f"インターネット接続に失敗しました。エラー: {e}"
        ) from e


def perform_connectivity_checks(
    device_ip: str, test_url: str = "https://www.google.com"
):
    """全ての接続チェックを実行します。"""
    router_ip = get_default_gateway()
    check_router(router_ip)
    check_device(device_ip)
    check_internet_connectivity(test_url)
    print("全ての接続チェックが成功しました。")
