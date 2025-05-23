@echo off
chcp 65001 >nul
setlocal

rem uvで仮想環境とパッケージをセットアップ
uv venv
uv pip install -e .

endlocal
