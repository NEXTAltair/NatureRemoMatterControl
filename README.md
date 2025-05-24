# 逆潮流が発生するとTPLinKのスマートプラグから給電を開始して､順潮流になると給電を停止するやつ

以下説明はコーパイロットワークスペースに書かせたやつなので明らかに間違ってる点もあるが特に修正はしない

Natureのトークンと､TPLinkのアカウントさえあれば取りあえず動く

Matterは対応してないのでリポジトリ名詐欺

WSL2を介してMatterの開発環境を整備するのはまた今度

# NatureRemoMatterControl

## プロジェクト概要

このプロジェクトは、Nature Remo APIを使用して家全体の電力消費量を測定し、逆潮流（電力の余剰）が発生した場合に python-kasa を使用してTP-Linkスマートプラグをオンにし、順潮流（電力の消費）に戻った場合にオフにする自動制御システムです。

### コンポーネント

- Nature Remo API: ECHONET Liteデバイスからデータを収集するために使用されます。
- TP-Linkスマートプラグ: python-kasaを使用して制御されます。
- 自動化ルール: 収集されたデータに基づいてデバイスを制御します。
- ダッシュボード: スマートホームデバイスを管理および監視します。

## セットアップ手順

1. リポジトリをクローンします:

    ```sh
    git clone https://github.com/NEXTAltair/NatureRemoMatterControl.git
    cd NatureRemoMatterControl
    ```

2. アプリケーションを開始します:

    PowerShellで以下のスクリプトを実行します。

    ```powershell
    ./start.ps1
    ```

    `start.ps1` が `uv` を使用して仮想環境のセットアップとアプリケーション (`nature-remo-con`) の実行を行います。
    初回実行時は必要なパッケージのインストールも行われます。

3. 設定ファイルと環境変数を準備します:

    - プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を参考にNature Remo APIのアクセストークンとTP-Linkの認証情報を記述します:

        ```env
        NATURE_REMO_TOKEN=YOUR_NATURE_REMO_ACCESS_TOKEN
        TPLINK_USERNAME=YOUR_SMART_PLUG_USER_NAME
        TPLINK_PASSWORD=YOUR_SMART_PLUG_PASSWORD
        DEFAULT_GATEWAY=YOUR_DEFAULT_GATEWAY_IP
        ```

    - `config/config.ini.template` を参考に `config/config.ini` ファイルを作成し、TP-LinkスマートプラグのIPアドレス等を設定します。
      `config/config.ini` の内容は以下のようになります:

        ```ini
        [TPLink]
        device_ip = 30,31

        # root_ip: ルートIPアドレスを指定します (現在は.envファイルのDEFAULT_GATEWAYを使用)
        # device_ip: デバイスIPの末尾二桁の数字をカンマ区切りで指定します
        # 例: device_ip = 01,02,03

        # 機密情報（Nature Remoトークン、TP-Linkのユーザー名・パスワード）は
        # .envファイルで環境変数として設定してください。
        ```
        **注意:** `device_ip` には、TP-LinkスマートプラグのIPアドレスの末尾2オクテット（例: `192.168.1.30` なら `30`）をカンマ区切りで指定します。デフォルトゲートウェイに基づいて完全なIPアドレスが組み立てられます。

4. TP-Linkスマートプラグをセットアップします:

    - TP-LinkスマートプラグがLANに接続されていることを確認します。
    - (必要であれば、[`src/nature_remo_controller/control.py`](src/nature_remo_controller/control.py) ファイル内のプラグ制御ロジックを確認・調整してください。)

## 使用方法

アプリケーションは `start.ps1` を実行することで起動し、設定に基づいて自動的に電力状況を監視し、TP-Linkスマートプラグを制御します。

以下は、個別の機能を直接実行する場合の参考情報です。
これらのスクリプトや関数は、通常、`main.py` (または `nature-remo-con` コマンド) を通じて間接的に呼び出されます。

### TP-Linkスマートプラグの制御 / Controlling TP-Link Smart Plugs

TP-Linkスマートプラグを直接制御するサンプルコードです。
実際の運用では、これらの認証情報は `.env` ファイルから読み込まれます。

```python
import asyncio
from src.nature_remo_controller.control import control_plug, login_tplinknbu
import os

async def main():
    # .envファイルから設定を読み込むことを想定
    ip_address = os.getenv('TPLINK_DEVICE_IP') # 例: '192.168.1.100' (実際にはconfig.iniと.envから組み立てられる)
    user_name = os.getenv('TPLINK_USERNAME')
    password = os.getenv('TPLINK_PASSWORD')

    if not all([ip_address, user_name, password]):
        print("必要な環境変数が設定されていません。(.envファイルを確認してください)")
        return

    dev = await login_tplinknbu(ip_address, user_name, password)
    if dev:
        await control_plug(dev, True)  # スマートプラグをオンにする
        await asyncio.sleep(5)  # 5秒待機
        await control_plug(dev, False) # スマートプラグをオフにする

if __name__ == "__main__":
    # 注意: このサンプルを直接実行する場合、適切なIPアドレスの取得ロジックが必要です。
    # 本プロジェクトでは、config.ini と .env の DEFAULT_GATEWAY からIPを組み立てます。
    asyncio.run(main())
```

### Nature Remo Eからのデータ取得 / Retrieving Data from Nature Remo E

Nature Remo Eからデータを取得するサンプルコードです。
実際の運用では、アクセストークンは `.env` ファイルから読み込まれます。

```python
from src.nature_remo_controller.monitoring import get_nature_remo_data, get_instant_power, display_instant_power
import os

# .envファイルから設定を読み込むことを想定
token = os.getenv('NATURE_REMO_TOKEN')

if not token:
    print("NATURE_REMO_TOKEN が設定されていません。(.envファイルを確認してください)")
else:
    # Nature Remo Eからデータを取得
    appliances = get_nature_remo_data(token)
    if appliances:
        data = get_instant_power(appliances)
        # 取得したデータを表示
        display_instant_power(data)
    else:
        print("Nature Remo Eからデータを取得できませんでした。")

```

## ライセンス / License

このプロジェクトはGPL-3.0ライセンスのもとで提供されています。LICENSE ファイルを参照してください。

## その他

- `src/nature_remo_controller/main.py` (`nature-remo-con` コマンドの実体): デバイスの制御と監視を調整するメインスクリプトです。設定ファイル (`config/config.ini`) と環境変数 (`.env`) を読み込み、それに基づいて動作します。
- `src/nature_remo_controller/control.py`: TP-Linkスマートプラグ制御用の関数を含みます。
- `src/nature_remo_controller/monitoring.py`: Nature Remo Eデバイスからのデータ取得および表示用の関数を含みます。
- `src/nature_remo_controller/logger_config.py`: ログ設定ファイルです。
- `tests`: ユニットテストが含まれています。
- `pyproject.toml`: プロジェクトの設定ファイルです。パッケージ情報や依存関係が記述されています。
- `uv.lock`: `uv` によって解決された依存関係のロックファイルです。

---

## English Summary

The code in this repository is designed to control TP-Link smart plugs and retrieve data from Nature Remo E devices. The system automatically turns on TP-Link smart plugs when surplus power generation is detected (reverse power flow) and turns them off when power consumption normalizes (forward power flow), based on data from the Nature Remo API.

Key components:

- `src/nature_remo_controller/main.py` (entry point: `nature-remo-con`): The main script that orchestrates device control and monitoring. It loads settings from `config/config.ini` and environment variables from `.env`.
- `src/nature_remo_controller/control.py`: Contains functions for controlling TP-Link smart plugs.
- `src/nature_remo_controller/monitoring.py`: Contains functions for retrieving and displaying data from Nature Remo E devices.
- `.env` (user-created): Stores sensitive information like API tokens and passwords.
- `config/config.ini`: Configuration file for TP-Link device IPs and other settings.
- `start.ps1`: PowerShell script to set up the virtual environment (using `uv`) and run the application.
- `pyproject.toml`: Project configuration file.

## License

This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

## LICENSE

```plaintext
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
```