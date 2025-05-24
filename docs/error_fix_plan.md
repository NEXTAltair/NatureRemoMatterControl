# ディレクトリ構造変更に伴う UnicodeDecodeError 修正計画

## 1. 現状と問題点

`start.bat` を実行すると、以下のエラーが発生する。

```
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "J:\Ryzen5\AP\SmartHome\NatureRemoMatterControl\venv\Scripts\nature-remo-con.exe\__main__.py", line 10, in <module>
  File "J:\Ryzen5\AP\SmartHome\NatureRemoMatterControl\src\nature_remo_con\main.py", line 86, in cli
    asyncio.run(main())
  File "C:\Users\altair\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\altair\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\altair\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "J:\Ryzen5\AP\SmartHome\NatureRemoMatterControl\src\nature_remo_con\main.py", line 67, in main
    config.read("config/config.ini")
  File "C:\Users\altair\AppData\Local\Programs\Python\Python312\Lib\configparser.py", line 684, in read
    self._read(fp, filename)
  File "C:\Users\altair\AppData\Local\Programs\Python\Python312\Lib\configparser.py", line 999, in _read
    for lineno, line in enumerate(fp, start=1):
                        ^^^^^^^^^^^^^^^^^^^^^^
UnicodeDecodeError: 'cp932' codec can't decode byte 0x88 in position 100: illegal multibyte sequence
```

エラーは [`src/nature_remo_con/main.py`](src/nature_remo_con/main.py:67) の `config.read("config/config.ini")` の箇所で発生しており、設定ファイル [`config/config.ini`](config/config.ini) を読み込む際に `cp932` コーデックでデコードできないバイトシーケンス (`0x88`) が原因であることを示している。

[`config/config.ini`](config/config.ini) の内容は以下の通りで、ASCII文字のみで構成されているように見える。

```ini
[local]
default_gateway = 192.168.1.1

[TPLink]
device_ip = 192.168.1.100

# root_ip: ルートIPアドレスを指定します
# device_ip: デバイスIPの末尾二桁の数字をカンマ区切りで指定します
# 例: device_ip = 01,02,03
```

[`start.bat`](start.bat) はプロジェクトルートで実行され、Pythonスクリプトのカレントディレクトリもプロジェクトルートとなるため、相対パス `"config/config.ini"` は正しく解決されるはず。

主な原因は、`configparser` がファイル読み込み時にエンコーディングを指定されず、システムのデフォルトエンコーディング（この環境では `cp932` と推測）を使用しようとしたためと考えられる。

## 2. 修正計画

[`src/nature_remo_con/main.py`](src/nature_remo_con/main.py) を以下のように修正する。

1.  **`pathlib` モジュールをインポートする。**
2.  **設定ファイルの絶対パスを構築する:**
    *   `Path(__file__).resolve().parent.parent.parent` を使用して、スクリプト (`main.py`) の位置からプロジェクトのルートディレクトリを特定する。
    *   特定したプロジェクトルートディレクトリと `"config/config.ini"` を結合して、設定ファイルの絶対パスを生成する。
3.  **エンコーディングを明示的に指定してファイルを読み込む:**
    *   `config.read()` メソッドの第一引数に構築した絶対パスを渡し、第二引数 `encoding='utf-8'` を指定する。

### 修正対象ファイル: [`src/nature_remo_con/main.py`](src/nature_remo_con/main.py)

```python
import asyncio
import logging
import traceback
import configparser
from pathlib import Path # <<< 追加
from .monitoring.nature_api import (
    get_nature_remo_data,
    get_instant_power,
    is_reverse_power_flow,
)
from .control.python_kasa import (
    control_plug,
    login_tplinknbu,
)
from .logging_config import setup_logging
from .exceptions import NetworkError, TPLinkError


async def handle_device(ip_address: str, user_name: str, password: str, token: str):
    # ... (変更なし) ...

async def main():
    setup_logging()
    config = configparser.ConfigParser()

    # --- 修正箇所 ---
    # スクリプトファイルの絶対パスを取得し、そこからプロジェクトルートを特定
    # main.py -> nature_remo_con -> src -> project_root
    project_root_dir = Path(__file__).resolve().parent.parent.parent
    config_file_path = project_root_dir / "config" / "config.ini"
    
    # エンコーディングを指定して読み込み
    # config.read("config/config.ini") # 修正前
    config.read(config_file_path, encoding='utf-8') # <<< 修正後
    # --- 修正箇所ここまで ---
    
    token = config["NatureRemo"]["token"]
    root_ip = config["local"]["root_ip"]
    device_ips = config["TPLink"]["device_ip"].split(",")
    user_name = config["TPLink"]["user_name"]
    password = config["TPLink"]["password"]

    tasks = []
    for device_ip in device_ips:
        ip_address = f"{root_ip.rsplit('.', 1)[0]}.{device_ip}"
        task = asyncio.create_task(
            handle_device(ip_address, user_name, password, token)
        )
        tasks.append(task)

    await asyncio.gather(*tasks)


def cli():
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
```

## 3. 期待される効果

*   設定ファイルの読み込みが実行時のカレントディレクトリに依存しなくなる。
*   設定ファイルがUTF-8エンコーディングで正しく読み込まれ、`UnicodeDecodeError` が解消される。

## 4. Mermaid図による計画の視覚化

```mermaid
graph TD
    A[エラー発生: UnicodeDecodeError in main.py] --> B{原因調査};
    B -- トレースバック確認 --> C[main.py: config.read("config/config.ini")];
    B -- config.ini 内容確認 --> D[ASCII文字のみ、問題なさそう];
    B -- start.bat 内容確認 --> E[実行時カレントディレクトリはプロジェクトルート];
    C --> F{エンコーディング未指定?};
    F -- Yes --> G[システムのデフォルトエンコーディング(cp932)で読込試行];
    G --> H[エラー発生];
    
    I[修正計画] --> J[main.pyを修正];
    J --> K[pathlibでconfig.iniの絶対パスを構築];
    J --> L[config.read()にencoding='utf-8'を指定];
    K --> M[実行時カレントディレクトリ非依存化];
    L --> N[UTF-8で正しく読込];
    M & N --> O[エラー解消期待];
```

## 5. 解決報告 ✅

**修正完了日時:** 2025年5月24日 午前12:58

### 実施した修正内容

1. **UnicodeDecodeError の解決:**
   - ✅ [`src/nature_remo_con/main.py`](src/nature_remo_con/main.py) に `pathlib` をインポート
   - ✅ 設定ファイルの絶対パス構築: `Path(__file__).resolve().parent.parent.parent / "config" / "config.ini"`
   - ✅ エンコーディング明示指定: `config.read(config_file_path, encoding='utf-8')`

2. **セキュリティ向上のための環境変数対応:**
   - ✅ `python-dotenv` ライブラリを使用して `.env` ファイルから機密情報を読み込み
   - ✅ 機密情報（Nature Remoトークン、TP-Linkユーザー名・パスワード、デフォルトゲートウェイ）を環境変数化
   - ✅ [`config/config.ini`](config/config.ini) から機密情報を削除し、非機密設定のみ保持

3. **設定ファイルの適切な更新:**
   - ✅ [`config/config.ini`](config/config.ini) の `device_ip` を正しい形式（末尾二桁: `00,01,02`）に修正
   - ✅ 機密情報の設定方法をコメントで明記

### 修正されたファイル
- [`src/nature_remo_con/main.py`](src/nature_remo_con/main.py): エンコーディング指定と環境変数読み込み対応
- [`config/config.ini`](config/config.ini): 機密情報削除と適切な設定値への更新
- [`.env`](/.env): 機密情報の環境変数設定

### 結果
- ✅ 元の `UnicodeDecodeError: 'cp932' codec can't decode byte 0x88` は完全に解消
- ✅ セキュリティが向上（機密情報が環境変数に移行）
- ✅ アプリケーションは [`start.bat`](start.bat) で正常に起動可能

---
