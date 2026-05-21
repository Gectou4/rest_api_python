class TestApi:
    def test_get_user(self, client):
        response = client.get("/user/1")
        assert response.status_code == 200
        data = response.get_json()
        assert "user_id" in data
        assert data["name"] == "G4"

    def test_get_user_task(self, client):
        response = client.get("/user/1/task")
        assert response.status_code == 200
        data = response.get_json()
        assert "user_id" in data
        assert "tasks" in data
        assert len(data["tasks"]) == 2

    def test_add_task(self, client):
        response = client.post("/task", data={"title": "New Task", "description": "Test"})
        assert response.status_code == 201
        data = response.get_json()
        assert "task_id" in data
        assert data["title"] == "New Task"

    def test_edit_task(self, client):
        response = client.post("/task/1", data={"title": "Updated Task"})
        assert response.status_code == 200
        data = response.get_json()
        assert data == 1

    def test_add_task_to_user(self, client):
        add_resp = client.post("/task", data={"title": "Task for User", "description": "Test"})
        task_id = add_resp.get_json()["task_id"]
        response = client.post(f"/user/1/task/{task_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data == 1

    def test_del_task_to_user(self, client):
        response = client.delete("/user/1/task/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data == 1

    def test_del_task(self, client):
        response = client.delete("/task/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data == 1
