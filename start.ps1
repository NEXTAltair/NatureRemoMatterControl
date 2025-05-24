#Requires -Version 5.0
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Checking for virtual environment..."
Write-Host "仮想環境を確認しています..."

# 仮想環境がなければ作成
if (-not (Test-Path -Path ".venv" -PathType Container)) {
    Write-Host "Creating a new virtual environment..."
    Write-Host "新規に仮想環境を作成しています..."
    # uvで仮想環境とパッケージをセットアップ
    # (uvコマンドがパスに通っている必要があります)
    uv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment."
        Pause
        exit 1
    }
    uv pip install -e .
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install packages."
        Pause
        exit 1
    }
}

Write-Host "Running the application..."
Write-Host "アプリケーションを実行しています..."

# アプリケーションを実行
uv run nature-remo-con

Pause 