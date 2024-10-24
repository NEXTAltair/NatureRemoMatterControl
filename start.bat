@echo off
REM venvディレクトリが存在するか確認
if not exist "venv" (
    REM install.batを実行
    call install.bat
)

REM 仮想環境をアクティブにする
call venv\Scripts\activate.bat

REM mainをasyncio.run(main())で実行
python -c "import asyncio; from main import main; asyncio.run(main())"

REM ウィンドウを開いたままにする
pause