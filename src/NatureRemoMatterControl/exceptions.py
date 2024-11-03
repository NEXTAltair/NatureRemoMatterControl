# exceptions.py
# ディレクトリ構造変更Ver
class NetworkError(Exception):
    """ネットワーク接続に関する基底エラークラス."""

    def __init__(self, message: str = "ネットワーク接続エラーが発生しました。"):
        super().__init__(message)


class RouterUnreachableError(NetworkError):
    """ルーターに到達できない場合の例外."""

    def __init__(self, router_ip: str, message: str = None):
        self.router_ip = router_ip
        if message is None:
            message = f"ルーター {router_ip} に到達できません。"
        super().__init__(message)


class DeviceUnreachableError(NetworkError):
    """指定されたデバイスに到達できない場合の例外."""

    def __init__(self, device_ip: str, message: str = None):
        self.device_ip = device_ip
        if message is None:
            message = f"指定されたIPアドレス {device_ip} に接続できません。"
        super().__init__(message)


class InternetConnectionError(NetworkError):
    """インターネット接続が利用できない場合の例外."""

    def __init__(self, message: str = "インターネットに接続できません。"):
        super().__init__(message)


class ConnectionTimeoutError(NetworkError):
    """接続試行がタイムアウトした場合の例外."""

    def __init__(self, target: str, timeout: float, message: str = None):
        self.target = target
        self.timeout = timeout
        if message is None:
            message = f"{target} への接続が {timeout} 秒でタイムアウトしました。"
        super().__init__(message)


class TPLinkError(Exception):
    """TPLinkデバイスに関するエラークラス."""

    def __init__(self, message: str = "TPLinkデバイスの操作に失敗しました。"):
        super().__init__(message)
