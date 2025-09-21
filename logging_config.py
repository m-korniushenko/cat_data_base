"""
Настройки логирования для Cat Database
Убирает лишние логи и оставляет только важную информацию
"""

import logging
import sys
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для логов"""
    
    # Цвета для разных уровней
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Добавляем цвет к уровню
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)

def setup_logging():
    """Настройка системы логирования"""
    
    # Создаем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Удаляем все существующие обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Создаем консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Настраиваем формат
    formatter = ColoredFormatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчик
    root_logger.addHandler(console_handler)
    
    # Отключаем лишние логи от внешних библиотек
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.error').setLevel(logging.WARNING)
    logging.getLogger('fastapi').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    logging.getLogger('asyncpg').setLevel(logging.WARNING)
    logging.getLogger('nicegui').setLevel(logging.INFO)
    
    # Настраиваем наш логгер
    app_logger = logging.getLogger('cat_database')
    app_logger.setLevel(logging.INFO)
    
    return app_logger

def log_info(message: str):
    """Логирование информационных сообщений"""
    logger = logging.getLogger('cat_database')
    logger.info(f"🐱 {message}")

def log_error(message: str):
    """Логирование ошибок"""
    logger = logging.getLogger('cat_database')
    logger.error(f"❌ {message}")

def log_success(message: str):
    """Логирование успешных операций"""
    logger = logging.getLogger('cat_database')
    logger.info(f"✅ {message}")

def log_warning(message: str):
    """Логирование предупреждений"""
    logger = logging.getLogger('cat_database')
    logger.warning(f"⚠️ {message}")
