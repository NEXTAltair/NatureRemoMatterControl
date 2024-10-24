@echo off
setlocal

rem Python 3.12のチェック / Python 3.12 check
Py -3.12 --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python 3.12 is required.
    exit /b 1
)

rem 仮想環境の作成 / Create virtual environment
set "VENV_DIR=%~dp0%venv"
if not exist "%VENV_DIR%\Scripts\python.exe" (
    Py -3.12 -m venv "%VENV_DIR%"
)

rem Python実行ファイルを使用してpipをアップグレード / Upgrade pip using Python executable
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip

rem 仮想環境を有効化 / Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

rem 依存パッケージのインストール / Install requirements
if exist requirements.txt (
    pip install -r requirements.txt
)

rem config.iniが存在しない場合、config.ini.templateをコピー / Copy config.ini.template to config.ini if not exists
if not exist "%~dp0config.ini" (
    copy "%~dp0config.ini.template" "%~dp0config.ini"
)

endlocal
