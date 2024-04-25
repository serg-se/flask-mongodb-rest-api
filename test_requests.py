from app import mongo

TASK = {
    "title": "Task1",
    "description": "Doing task 1",
    "done": False,
}


def create_task():
    return mongo.db.tasks.insert_one(TASK.copy()).inserted_id


def test_get(mongo_teardown, flask_client):
    create_task()
    response = flask_client.get(
        "/todo/api/v1.0/tasks",
    )
    assert response.status_code == 200
    assert response.is_json is True
    assert len(response.json) == 1
    assert response.json[0]["title"] == TASK["title"]
    assert response.json[0]["description"] == TASK["description"]
    assert response.json[0]["done"] == TASK["done"]


def test_get_id(flask_client):
    insert_id = create_task()
    response = flask_client.get(
        f"/todo/api/v1.0/tasks/{insert_id}",
    )
    assert response.status_code == 200
    assert response.json["title"] == TASK["title"]
    assert response.json["description"] == TASK["description"]
    assert response.json["done"] == TASK["done"]


def test_post(flask_client):
    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=TASK,
    )
    assert response.status_code == 201
    assert response.is_json is True
    assert response.json["title"] == TASK["title"]
    assert response.json["description"] == TASK["description"]
    assert response.json["done"] == TASK["done"]


def test_put(flask_client):
    insert_id = create_task()
    updated_task = {
        "title": "New title",
        "description": "New description",
        "done": True,
    }

    response = flask_client.put(
        f"/todo/api/v1.0/tasks/{insert_id}",
        json=updated_task,
    )
    assert response.status_code == 200
    assert response.is_json is True
    assert response.json["title"] == updated_task["title"]
    assert response.json["description"] == updated_task["description"]
    assert response.json["done"] == updated_task["done"]


def test_404_get(flask_client):
    insert_id = "66298b9a4ffe7e127757708f"
    response = flask_client.get(
        f"/todo/api/v1.0/tasks/{insert_id}",
    )
    assert response.status_code == 404
    assert response.json["error"] == "Not Found"
    assert response.json["description"] == f"Task with ID {insert_id} not found."


def test_404_put(flask_client):
    updated_task = {
        "title": "New title",
        "description": "New description",
        "done": True,
    }
    insert_id = "66298b9a4ffe7e127757708f"
    response = flask_client.put(
        f"/todo/api/v1.0/tasks/{insert_id}",
        json=updated_task,
    )
    assert response.status_code == 404
    assert response.json["error"] == "Not Found"
    assert response.json["description"] == f"Task with ID {insert_id} not found."
