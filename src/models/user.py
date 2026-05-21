from src.models.base import DB, BaseModel


class User(BaseModel):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.email: str = ""

    def load(self, record_id: int) -> bool:
        conn = DB.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE user_id = %s", (record_id,))
            row = cursor.fetchone()
        if row:
            self.id = row["user_id"]
            self.name = row["name"]
            self.email = row["email"]
            self._loaded = True
            return True
        return False

    def get_task(self):
        from src.models.user_task import UserTask

        return UserTask.get_task_by_user(self)

    def to_dict(self) -> dict:
        return {
            "user_id": self.id,
            "name": self.name,
            "email": self.email,
        }
