import threading
from abc import ABC, abstractmethod

import pymysql

from src.config.db import DBConfig


class DB:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_connection(cls) -> pymysql.Connection:
        if cls._instance is None or not cls._is_alive():
            with cls._lock:
                if cls._instance is None or not cls._is_alive():
                    cls._instance = pymysql.connect(**DBConfig.get_connection_params())
        return cls._instance

    @classmethod
    def _is_alive(cls) -> bool:
        if cls._instance is None:
            return False
        try:
            cls._instance.ping(reconnect=False)
            return True
        except pymysql.err.Error:
            return False


class BaseModel(ABC):
    def __init__(self):
        self.id: int = 0
        self._loaded: bool = False

    @abstractmethod
    def load(self, record_id: int) -> bool:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def is_loaded(self) -> bool:
        return self._loaded
