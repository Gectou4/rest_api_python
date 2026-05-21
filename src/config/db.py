import os

import pymysql.cursors


class DBConfig:
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PWD", "")
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "3306"))
    database: str = os.getenv("DB_NAME", "rest_api")

    @classmethod
    def get_connection_params(cls) -> dict:
        return {
            "host": cls.host,
            "port": cls.port,
            "user": cls.user,
            "password": cls.password,
            "database": cls.database,
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": True,
        }
