import time

import pymysql
import pytest

from src.app import app
from src.config.db import DBConfig


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def db_connection():
    params = DBConfig.get_connection_params()
    for _ in range(30):
        try:
            conn = pymysql.connect(**params)
            yield conn
            conn.close()
            return
        except pymysql.err.OperationalError:
            time.sleep(1)
    raise ConnectionError("Cannot connect to MySQL after 30 retries")


@pytest.fixture(autouse=True)
def reset_database(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_task")
        cursor.execute("DELETE FROM task")
        cursor.execute("DELETE FROM user")
        cursor.execute("ALTER TABLE user_task AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE task AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE user AUTO_INCREMENT = 1")
        cursor.execute("INSERT INTO user (user_id, name, email) VALUES (1, 'G4', 'g4@example.com')")
        cursor.execute(
            "INSERT INTO task (task_id, title, description, creation_date, status) VALUES "
            "(1, 'Task 1', 'Description of task 1', NOW(), 1), "
            "(2, 'Task 2', 'Description of task 2', NOW(), 2)"
        )
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (1, 1), (1, 2)")
    db_connection.commit()
