@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

rem 仮想環境がなければ作成
if not exist ".venv" (
    echo Creating a new virtual environment...
    echo 新規に仮想環境を作成しています...
    call install.bat
)

echo Running the application...
echo アプリケーションを実行しています...
uv run nature-remo-con
if %errorlevel% neq 0 (
    echo The application exited with an error. Please check the logs for more information.
    echo アプリケーションがエラーで終了しました。詳細はログを確認してください。
    pause
    exit /b 1
)

echo Application closed.
echo アプリケーションが終了しました。
pause