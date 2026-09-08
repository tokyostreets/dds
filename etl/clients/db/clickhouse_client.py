import threading
from clickhouse_connect import get_client
from etl.config.config import settings


class ClickHouseConnection:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_client(cls): 
        with cls._lock:
            if cls._instance is None:
                cls._instance = get_client(
                    host=settings.CLICKHOUSE.clickhouse_host,
                    port=settings.CLICKHOUSE.clickhouse_port,
                    username=settings.CLICKHOUSE.clickhouse_user,
                    password=settings.CLICKHOUSE.clickhouse_password,
                    secure=settings.CLICKHOUSE.clickhouse_secure,  
                )

            return cls._instance