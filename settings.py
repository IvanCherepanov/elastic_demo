# Настройка базовой конфигурации логирования
import logging
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_port: int
    elasticsearch_cont_name: str
    elasticsearch_port_int: int
    elasticsearch_server: str

    log_file: Optional[str] = 'my_app.log'
    log_level: Optional[int] = logging.INFO

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

logging.basicConfig(filename=config.log_file,
                    level=config.log_level,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
