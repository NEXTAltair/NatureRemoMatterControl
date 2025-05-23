# 逆潮流が発生するとTPLinKのスマートプラグから給電を開始して､順潮流になると給電を停止するやつ

以下説明はコーパイロットワークスペースに書かせたやつなので明らかに間違ってる点もあるが特に修正はしない

Natureのトークンと､TPLinkのアカウントさえあれば取りあえず動く

Matterは対応してないのでリポジトリ名詐欺

WSL2を介してMatterの開発環境を整備するのはまた今度

# NatureRemoMatterControl

## プロジェクト概要

このプロジェクトは、[Nature Remo API](path/to/NatureRemoAPI)を使用して家全体の電力消費量を測定し、[python-kasa](https://github.com/python-kasa/python-kasa)を使用してTP-Linkスマートプラグを制御する方法を示しています。Matterプロトコルを活用してスマートホームデバイスを管理および監視します。

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

    [start.bat](start.bat)

    `start.bat` が仮想環境のセットアップとアプリケーションの実行を行います。

3. Nature Remo APIのアクセストークンとTP-LinkスマートプラグのIPアドレスを設定します:

    - Nature Remo開発者ポータルからアクセストークンを取得します。
    - プロジェクトのルートディレクトリに [`config.ini`](config.ini) ファイルを作成し、以下の内容を記述します:

        ```ini
        [local]
        root_ip = YOUR_LOCAL_IP

        [NatureRemo]
        token = YOUR_ACCESS_TOKEN

        [TPLink]
        user_name = YOUR_SMART_PLUG_USER_NAME
        password = YOUR_SMART_PLUG_PASSWORD
        ```

4. TP-Linkスマートプラグをセットアップします:

    - TP-LinkスマートプラグがLANに接続されていることを確認します。
    - [`control.py`](control.py) ファイルの指示に従ってスマートプラグを設定します。

## 使用方法

### TP-Linkスマートプラグの制御 / Controlling TP-Link Smart Plugs

#### 日本語

TP-Linkスマートプラグを制御するには、以下の手順に従います:

1. [`control.py`](control.py) ファイルから必要な関数をインポートします。
2. 提供された関数を使用して、要件に基づいてスマートプラグをオン/オフします。

**例:**

```python
import asyncio
from control import control_plug, login_tplinknbu

async def main():
    ip_address = '192.168.1.100'
    user_name = 'test_user'
    password = 'test_password'

    dev = await login_tplinknbu(ip_address, user_name, password)
    if dev:
        await control_plug(dev, True, ip_address)  # スマートプラグをオンにする
        await asyncio.sleep(5)  # 5秒待機
        await control_plug(dev, False, ip_address)  # スマートプラグをオフにする

asyncio.run(main())
```

#### English

To control TP-Link smart plugs, follow these steps:

1. Import the necessary functions from the control.py file.

2. Use the provided functions to turn the smart plugs on/off based on your requirements.

**Example:**

```python
import asyncio
from control import control_plug, login_tplinknbu

async def main():
    ip_address = '192.168.1.100'
    user_name = 'test_user'
    password = 'test_password'

    dev = await login_tplinknbu(ip_address, user_name, password)
    if dev:
        await control_plug(dev, True, ip_address)  # Turn on the smart plug
        await asyncio.sleep(5)  # Wait for 5 seconds
        await control_plug(dev, False, ip_address)  # Turn off the smart plug

asyncio.run(main())
```

### Nature Remo Eからのデータ取得 / Retrieving Data from Nature Remo E

#### 日本語

Nature Remo Eからデータを取得するには、以下の手順に従います:

1. monitoring.py

 ファイルから必要な関数をインポートします。
2. 提供された関数を使用してデータを取得し、表示します。

**例:**

```python
from monitoring import get_nature_remo_data, display_instant_power

# Nature Remo Eからデータを取得
token = 'YOUR_ACCESS_TOKEN'
appliances = get_nature_remo_data(token)
data = get_instant_power(appliances)

# 取得したデータを表示
display_instant_power(data)
```

#### English

To retrieve data from Nature Remo E, follow these steps:

1. Import the necessary functions from the monitoring.py

 file.
2. Use the provided functions to retrieve and display the data.

**Example:**

```python
from monitoring import get_nature_remo_data, display_instant_power

# Retrieve data from Nature Remo E
token = 'YOUR_ACCESS_TOKEN'
appliances = get_nature_remo_data(token)
data = get_instant_power(appliances)

# Display the retrieved data
display_instant_power(data)
```

## ライセンス / License

このプロジェクトはGPL-3.0ライセンスのもとで提供されています。LICENSE ファイルを参照してください。

## その他

- main.py

: デバイスの制御と監視を調整するメインスクリプトです。
- logging_config.py

: ログ設定ファイルです。
- test

: ユニットテストが含まれています。

---

## English Summary

The code in this repository is designed to control TP-Link smart plugs and retrieve data from Nature Remo E devices. The main components include:

- control.py

: Contains functions to control TP-Link smart plugs using the Matter protocol.
- monitoring.py

: Contains functions to retrieve and display data from Nature Remo E devices.
- main.py

: The main script that orchestrates the control and monitoring of devices.
- config.ini

: Configuration file to store Nature Remo API access token and TP-Link smart plug IP address.

## License

This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

## LICENSE

```plaintext
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
```