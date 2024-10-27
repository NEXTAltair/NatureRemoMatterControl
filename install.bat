@echo off
setlocal

rem 仮想環境の作成 / Create virtual environment
set "VENV_DIR=%~dp0%venv"
if not exist "%VENV_DIR%\Scripts\python.exe" (
    Py -m venv "%VENV_DIR%"
)

rem Python実行ファイルを使用してpipをアップグレード / Upgrade pip using Python executable
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip

rem 仮想環境を有効化 / Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

rem 依存パッケージのインストール / Install requirements
if exist requirements.txt (
    pip install -r requirements.txt
)

REM config.iniが存在しない場合、config.ini.templateをコピー / Copy config.ini.template to config.ini if not exists
if not exist "%~dp0config.ini" (
    copy "%~dp0config.ini.template" "%~dp0config.ini"
    echo 初期設定を入力してください:

    rem [local] セクション
    set /p root_ip=ルートIPアドレスを入力してください (root_ip):

    rem [NatureRemo] セクション
    set /p token=NatureRemoのアクセストークンを入力してください (token):

    rem [TPLink] セクション
    set /p user_name=TPLinkのユーザー名を入力してください (user_name):
    set /p password=TPLinkのパスワードを入力してください (password):
    set /p device_ip=TPLinkデバイスのIPアドレス末尾二桁をカンマ区切りで入力してください (device_ip, 例: 1,2,3):

    REM 設定をconfig.iniに書き込む
    (
        echo [local]
        echo root_ip=%root_ip%
        echo.
        echo [NatureRemo]
        echo token=%token%
        echo.
        echo [TPLink]
        echo user_name=%user_name%
        echo password=%password%
        echo device_ip=%device_ip%
    ) > "%~dp0config.ini"
)

endlocal
