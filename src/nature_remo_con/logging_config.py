from loguru import logger
import sys

def setup_logging():
    """Loguruを使用したロギング設定(日本語対応)"""
    # 既存のハンドラーを削除
    logger.remove()
    
    # コンソール出力(UTF-8対応、カラー表示)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # ファイル出力(UTF-8明示指定、ローテーション対応)
    logger.add(
        "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        encoding="utf-8",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    
    return logger
