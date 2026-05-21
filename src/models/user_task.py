from src.models.base import DB
from src.models.task import Task
from src.models.task_status import TaskStatus


class UserTask:
    def __init__(self):
        self.user_id: int = 0
        self.task_list: list[Task] = []

    def save(self) -> bool:
        conn = DB.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM user_task WHERE user_id = %s", (self.user_id,))
                for task in self.task_list:
                    cursor.execute(
                        "INSERT INTO user_task (user_id, task_id) VALUES (%s, %s)",
                        (self.user_id, task.id),
                    )
            return True
        except Exception:
            conn.rollback()
            return False

    def delete_task(self, task_id: int) -> bool:
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_task WHERE user_id = %s AND task_id = %s",
                (self.user_id, task_id),
            )
        return True

    def add_task_id(self, task_id: int):
        task = Task()
        task.load(task_id)
        if not self.has_task(task_id):
            self.task_list.append(task)

    def remove_task_id(self, task_id: int):
        self.task_list = [t for t in self.task_list if t.id != task_id]

    def has_task(self, task_id: int) -> bool:
        return any(t.id == task_id for t in self.task_list)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "tasks": {str(t.id): t.to_dict() for t in self.task_list},
        }

    @staticmethod
    def get_task_by_user(user) -> "UserTask":
        user_task = UserTask()
        user_task.user_id = user.id
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT t.* FROM task t INNER JOIN user_task ut ON t.task_id = ut.task_id WHERE ut.user_id = %s",
                (user.id,),
            )
            rows = cursor.fetchall()
        for row in rows:
            task = Task()
            task.id = row["task_id"]
            task.title = row["title"]
            task.description = row["description"]
            task.creation_date = row["creation_date"]
            task.status = TaskStatus(row["status"])
            task._loaded = True
            user_task.task_list.append(task)
        return user_task
