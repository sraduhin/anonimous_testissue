import os
from logging import config as logging_config

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv("PROJECT_NAME", "Тестовое задание")
PROJECT_DESC = os.getenv(
    "PROJECT_DESC", "Тестовое задание на позицию python-dev"
)
PROJECT_VERSION = os.getenv("PROJECT_VERSION", "1.0.0")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
