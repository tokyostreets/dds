import redis 
import threading

from etl.config.config import settings


class RedisConnection: 
    _instance = None
    _lock = threading.Lock() 

    @classmethod
    def get_client(cls): 
        with cls._lock:
            if cls._instance is None: 
                cls._instance = redis.Redis( 
                    host = settings.REDIS.redis_host,
                    port = settings.REDIS.redis_port,
                    db = settings.REDIS.redis_db,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                    retry_on_timeout=True,
                )

        return cls._instance