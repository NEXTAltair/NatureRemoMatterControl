# 逆潮流が発生するとTPLinKのスマートプラグから給電を開始して､順潮流になると給電を停止するやつ

以下説明はコーパイロットワークスペースに書かせたやつなので明らかに間違ってる点もあるが特に修正はしない

Natureのトークンと､TPLinkのアカウントさえあれば取りあえず動くので


# Nature Remo API and TP-Link Smart Plug Control

This project demonstrates how to use the Nature Remo API to measure the power consumption of your entire home and control TP-Link smart plugs using the Matter protocol.

## Project Description

The project involves the following components:
- Nature Remo API: Used to gather data from ECHONET Lite devices.
- TP-Link Smart Plugs: Controlled using the Matter protocol.
- Automation Rules: Developed to control devices based on the data collected.
- Dashboard: Created to manage and monitor the smart home devices.

このプロジェクトは、Nature Remo APIを使用して家全体の電力消費量を測定し、Matterプロトコルを使用してTP-Linkスマートプラグを制御する方法を示しています。

### プロジェクトの説明

プロジェクトには以下のコンポーネントが含まれます：
- Nature Remo API: ECHONET Liteデバイスからデータを収集するために使用されます。
- TP-Linkスマートプラグ: Matterプロトコルを使用して制御されます。
- 自動化ルール: 収集されたデータに基づいてデバイスを制御するために開発されました。

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. Install the required libraries:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your Nature Remo API access token and TP-Link Smart Plug IP address:
   - Obtain your access token from the Nature Remo developer portal.
   - Create a `config.ini` file in the root directory of the project with the following content:
     ```
     [NatureRemo]
     token = YOUR_ACCESS_TOKEN

     [TPLink]
     ip_address = YOUR_SMART_PLUG_IP_ADDRESS
     user_name = YOUR_SMART_PLUG_USER_NAME
     password = YOUR_SMART_PLUG_PASSWORD
     ```

4. Set up your TP-Link Smart Plug:
   - Ensure your TP-Link Smart Plug is connected to your LAN.
   - Follow the instructions in the `control.py` file to configure the smart plug.

### セットアップ手順

1. リポジトリをクローンします：
   ```sh
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. 必要なライブラリをインストールします：
   ```sh
   pip install -r requirements.txt
   ```

3. Nature Remo APIのアクセストークンとTP-LinkスマートプラグのIPアドレスを設定します：
   - Nature Remo開発者ポータルからアクセストークンを取得します。
   - プロジェクトのルートディレクトリに`config.ini`ファイルを作成し、以下の内容を記述します：
     ```
     [NatureRemo]
     token = YOUR_ACCESS_TOKEN

     [TPLink]
     ip_address = YOUR_SMART_PLUG_IP_ADDRESS
     user_name = YOUR_SMART_PLUG_USER_NAME
     password = YOUR_SMART_PLUG_PASSWORD
     ```

4. TP-Linkスマートプラグを設定します：
   - TP-LinkスマートプラグがLANに接続されていることを確認します。
   - `control.py`ファイルの指示に従ってスマートプラグを設定します。

## Usage Instructions

### Controlling TP-Link Smart Plugs

To control TP-Link smart plugs using the Matter protocol, follow these steps:

1. Import the necessary functions from the `control.py` file.
2. Use the provided functions to turn on/off the smart plugs based on your requirements.

Example:
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

### TP-Linkスマートプラグの制御

Matterプロトコルを使用してTP-Linkスマートプラグを制御するには、以下の手順に従います：

1. `control.py`ファイルから必要な関数をインポートします。
2. 提供された関数を使用して、要件に基づいてスマートプラグをオン/オフします。

例：
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

### Retrieving Data from Nature Remo E

To retrieve data from Nature Remo E, follow these steps:

1. Import the necessary functions from the `monitoring.py` file.
2. Use the provided functions to retrieve and display the data.

Example:
```python
from monitoring import get_nature_remo_data, display_instant_power

# Retrieve data from Nature Remo E
token = 'YOUR_ACCESS_TOKEN'
appliances = get_nature_remo_data(token)
data = get_instant_power(appliances)

# Display the retrieved data
display_instant_power(data)
```

### Nature Remo Eからデータを取得する

Nature Remo Eからデータを取得するには、以下の手順に従います：

1. `monitoring.py`ファイルから必要な関数をインポートします。
2. 提供された関数を使用してデータを取得し、表示します。

例：
```python
from monitoring import get_nature_remo_data, display_instant_power

# Nature Remo Eからデータを取得
token = 'YOUR_ACCESS_TOKEN'
appliances = get_nature_remo_data(token)
data = get_instant_power(appliances)

# 取得したデータを表示
display_instant_power(data)
```

The example code provided in the repository demonstrates this process. The code is located in the `1.APIで取得できるプロパティを確認する` section. It sets the access token, sends a GET request to the API endpoint, and prints the JSON response. The response includes details about appliances such as smart meters and electric water heaters, along with their properties and updated values.

For more details, refer to the code in the `1.APIで取得できるプロパティを確認する` section.

リポジトリに提供されているサンプルコードは、このプロセスを示しています。コードは`1.APIで取得できるプロパティを確認する`セクションにあります。アクセストークンを設定し、APIエンドポイントにGETリクエストを送信し、JSONレスポンスを出力します。レスポンスには、スマートメーターや電気温水器などの機器の詳細とそのプロパティおよび更新された値が含まれています。

詳細については、`1.APIで取得できるプロパティを確認する`セクションのコードを参照してください。

## Summary of Code Functionality

### English

The code in this repository is designed to control TP-Link smart plugs and retrieve data from Nature Remo E devices. The main components include:

- `control.py`: Contains functions to control TP-Link smart plugs using the Matter protocol.
- `monitoring.py`: Contains functions to retrieve and display data from Nature Remo E devices.
- `main.py`: The main script that orchestrates the control and monitoring of devices.
- `config.ini`: Configuration file to store Nature Remo API access token and TP-Link smart plug IP address.

### 日本語

このリポジトリのコードは、TP-Linkスマートプラグを制御し、Nature Remo Eデバイスからデータを取得するように設計されています。主なコンポーネントは以下の通りです：

- `control.py`: Matterプロトコルを使用してTP-Linkスマートプラグを制御する関数が含まれています。
- `monitoring.py`: Nature Remo Eデバイスからデータを取得し、表示する関数が含まれています。
- `main.py`: デバイスの制御と監視を調整するメインスクリプトです。
- `config.ini`: Nature Remo APIのアクセストークンとTP-LinkスマートプラグのIPアドレスを保存するための設定ファイルです。
