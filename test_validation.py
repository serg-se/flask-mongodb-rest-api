TASK = {
    "title": "Task1",
    "description": "Doing task 1",
    "done": False,
}


def test_no_title(flask_client):
    task = TASK.copy()
    del task["title"]

    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=task,
    )

    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert response.json["description"] == "Field required."


def test_empty_title(flask_client):
    task = TASK.copy()
    task["title"] = ""

    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=task,
    )

    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert response.json["description"] == "Should not be empty."


def test_empty_description(flask_client):
    task = TASK.copy()
    task["description"] = ""

    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=task,
    )
    assert response.status_code == 201


def test_title_too_long(flask_client):
    task = TASK.copy()
    task["title"] = "e" * 30

    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=task,
    )
    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert response.json["description"] == "Cannot be longer then 20 characters."


def test_wrong_title_format(flask_client):
    task = TASK.copy()
    task["title"] = None

    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=task,
    )

    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert response.json["description"] == "Input should be a valid string."


def test_wrong_done_format(flask_client):
    task = TASK.copy()
    task["done"] = 6

    response = flask_client.post(
        "/todo/api/v1.0/tasks",
        json=task,
    )
    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert (
        response.json["description"]
        == "Input should be a valid boolean, unable to interpret input."
    )


def test_wrong_id_format(flask_client):
    insert_id = "67"
    response = flask_client.get(
        f"/todo/api/v1.0/tasks/{insert_id}",
    )
    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert (
        response.json["description"]
        == "Is not a valid ObjectId, it must be a 24-character hex string."
    )


def test_empty_id(flask_client):
    insert_id = ""
    response = flask_client.get(
        f"/todo/api/v1.0/tasks/{insert_id}",
    )
    assert response.status_code == 404
    assert response.json["error"] == "Not Found"
