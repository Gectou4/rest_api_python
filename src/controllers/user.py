from src.controllers.base import BaseController
from src.models.user import User


class UserController(BaseController):
    def get_index(self, user_id: int):
        user = User()
        if not user.load(user_id):
            return self.json_response("No user found", 404)
        return self.json_response(user.to_dict())

    def get_user_task(self, user_id: int):
        user = User()
        if not user.load(user_id):
            return self.json_response("No user found", 404)
        user_task = user.get_task()
        return self.json_response(user_task.to_dict())
