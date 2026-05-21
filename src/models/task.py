from datetime import datetime

from src.models.base import DB, BaseModel
from src.models.task_status import TaskStatus


class Task(BaseModel):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.description: str = ""
        self.creation_date: datetime = datetime.now()
        self.status: TaskStatus = TaskStatus.Backlog

    def load(self, record_id: int) -> bool:
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM task WHERE task_id = %s", (record_id,))
            row = cursor.fetchone()
        if row:
            self.id = row["task_id"]
            self.title = row["title"]
            self.description = row["description"]
            self.creation_date = row["creation_date"]
            self.status = TaskStatus(row["status"])
            self._loaded = True
            return True
        return False

    def save(self) -> bool:
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            if self.id == 0:
                cursor.execute(
                    "INSERT INTO task (title, description, creation_date, status) VALUES (%s, %s, %s, %s)",
                    (self.title, self.description, self.creation_date, int(self.status)),
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE task SET title=%s, description=%s, status=%s WHERE task_id=%s",
                    (self.title, self.description, int(self.status), self.id),
                )
        return True

    def delete(self) -> bool:
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM task WHERE task_id = %s", (self.id,))
        return True

    @staticmethod
    def get_all() -> list[dict]:
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM task")
            return cursor.fetchall()

    def to_dict(self) -> dict:
        return {
            "task_id": self.id,
            "status": int(self.status),
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
