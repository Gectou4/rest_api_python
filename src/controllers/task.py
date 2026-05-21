from datetime import datetime

from flask import request

from src.controllers.base import BaseController
from src.models.task import Task
from src.models.task_status import TaskStatus
from src.models.user import User
from src.models.user_task import UserTask


class TaskController(BaseController):
    def post_add_task(self):
        data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
        title = data.get("title", "").strip()
        if not title:
            return self.json_response("Title is required", 400)

        task = Task()
        task.title = title
        task.description = data.get("description", "").strip()
        task.status = TaskStatus(int(data["status"])) if "status" in data else TaskStatus.Backlog
        task.creation_date = datetime.now()
        task.save()
        return self.json_response(task.to_dict(), 201)

    def put_add_task(self):
        return self.post_add_task()

    def post_edit_task(self, task_id: int):
        data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
        task = Task()
        if not task.load(task_id):
            return self.json_response("Task not found", 400)

        if "title" in data:
            task.title = data["title"].strip()
        if "description" in data:
            task.description = data["description"].strip()
        if "status" in data:
            task.status = TaskStatus(int(data["status"]))

        task.save()
        return self.json_response(1)

    def put_edit_task(self, task_id: int):
        return self.post_edit_task(task_id)

    def delete_task(self, task_id: int):
        task = Task()
        if not task.load(task_id):
            return self.json_response("Task not found", 400)
        task.delete()
        return self.json_response(1)

    def post_add_task_to_user(self, user_id: int, task_id: int):
        user = User()
        if not user.load(user_id):
            return self.json_response("User not found", 400)

        task = Task()
        if not task.load(task_id):
            return self.json_response("Task not found", 400)

        user_task = UserTask.get_task_by_user(user)
        user_task.add_task_id(task_id)
        user_task.save()
        return self.json_response(1)

    def put_add_task_to_user(self, user_id: int, task_id: int):
        return self.post_add_task_to_user(user_id, task_id)

    def delete_user_task(self, user_id: int, task_id: int):
        user = User()
        if not user.load(user_id):
            return self.json_response("User not found", 400)

        user_task = UserTask()
        user_task.user_id = user_id
        user_task.delete_task(task_id)
        return self.json_response(1)
