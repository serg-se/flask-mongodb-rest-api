from bson import ObjectId
from flask import request
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from app import mongo
from app.apis.errors import abort_descriptive
from app.apis.validators import TaskIDModel, TaskModel, error_message

ns = Namespace("Tasks", "APIs related to the to-do list module", path="/todo/api/v1.0/tasks")
task_model = ns.model(
    "Detail",
    {
        "title": fields.String,
        "description": fields.String,
        "done": fields.Boolean,
        "uri": fields.Url("api.task"),
    },
)


@ns.route("", endpoint="tasks")
class TaskListAPI(Resource):
    """API for handling the Task list resource."""

    @staticmethod
    @ns.doc(
        responses={
            200: "Get the task list",
        },
    )
    @ns.marshal_list_with(task_model)
    def get():
        """Get all tasks."""
        tasks = mongo.db.tasks.find(limit=100)
        return [*tasks]

    @staticmethod
    @ns.doc(
        responses={
            400: "Invalid data format",
            404: "Task not found",
            200: "Get the task list",
        },
    )
    @ns.marshal_with(task_model, code=201)
    def post():
        """Add a new task."""

        # Validate data.
        request_data = request.get_json()
        try:
            task = TaskModel(**request_data).model_dump()
        except ValidationError as e:
            message = error_message(e)
            abort_descriptive(ns, 400, message)

        # Create task.
        new_task = mongo.db.tasks.insert_one(task)
        created_task = mongo.db.tasks.find_one({"_id": new_task.inserted_id})
        return created_task, 201


@ns.route("/<string:_id>", endpoint="task")
class TaskAPI(Resource):
    """API for handling the single Task resource."""

    @staticmethod
    @ns.doc(
        params={"_id": "Task ID"},
        responses={
            400: "Invalid data format",
            404: "Task not found",
            200: "Get the task list",
        },
    )
    @ns.marshal_with(task_model)
    def get(_id):
        """Get task by a given ID."""

        # Validate id.
        try:
            _id = TaskIDModel(id=_id).model_dump()["id"]
        except ValidationError as e:
            message = error_message(e)
            abort_descriptive(ns, 400, message)

        # Retrieve task.
        if (task := mongo.db.tasks.find_one({"_id": ObjectId(_id)})) is not None:
            return task
        abort_descriptive(ns, 404, f"Task with ID {_id} not found.")

    @staticmethod
    @ns.doc(
        params={"_id": "Task ID"},
        responses={
            400: "Invalid data format",
            404: "Task not found",
            200: "Get the task list",
        },
    )
    @ns.marshal_with(task_model)
    def put(_id):
        """Update a task with a given ID."""

        # Validate id.
        try:
            _id = TaskIDModel(id=_id).model_dump()["id"]
        except ValidationError as e:
            message = error_message(e)
            abort_descriptive(ns, 400, message)

        # Validate data.
        request_data = request.get_json()
        try:
            task = TaskModel(**request_data).model_dump()
        except ValidationError as e:
            message = error_message(e)
            abort_descriptive(ns, 400, message)

        # Update task.
        update_result = mongo.db.tasks.update_one({"_id": ObjectId(_id)}, {"$set": task})
        if update_result.modified_count == 0:
            abort_descriptive(ns, 404, f"Task with ID {_id} not found.")

        # Retrieve task.
        if (existing_book := mongo.db.tasks.find_one({"_id": ObjectId(_id)})) is not None:
            return existing_book
        abort_descriptive(ns, 404, f"Task with ID {_id} not found.")
