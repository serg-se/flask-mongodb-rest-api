from bson import ObjectId
from flask import request
from flask_restful import Resource, fields, marshal
from pydantic import ValidationError

from app import api, mongo
from app.errors.handlers import json_error_response
from app.main.validators import TaskIDModel, TaskModel, error_message

task_fields = {
    "title": fields.String,
    "description": fields.String,
    "done": fields.Boolean,
    "uri": fields.Url("main.task"),
}


class TaskListAPI(Resource):

    @staticmethod
    def get():
        """Get all tasks."""
        tasks = mongo.db.tasks.find(limit=100)
        return [marshal(task, task_fields) for task in tasks]

    @staticmethod
    def post():
        """Add a new task to the database."""
        request_data = request.get_json()
        try:
            task = TaskModel(**request_data).model_dump()

        except ValidationError as e:
            message = error_message(e)
            return json_error_response(400, description=message)

        new_task = mongo.db.tasks.insert_one(task)
        created_task = mongo.db.tasks.find_one({"_id": new_task.inserted_id})
        return marshal(created_task, task_fields), 201


class TaskAPI(Resource):

    @staticmethod
    def get(_id):
        """Get tasks by a given ID."""
        try:
            _id = TaskIDModel(id=_id).model_dump()["id"]
        except ValidationError as e:
            message = error_message(e)
            return json_error_response(400, description=message)

        if (task := mongo.db.tasks.find_one({"_id": ObjectId(_id)})) is not None:
            return marshal(task, task_fields)

        return json_error_response(404, description=f"Task with ID {_id} not found.")

    @staticmethod
    def put(_id):
        """Update a task with a given ID in the database."""
        try:
            _id = TaskIDModel(id=_id).model_dump()["id"]
        except ValidationError as e:
            message = error_message(e)
            return json_error_response(400, description=message)

        request_data = request.get_json()
        try:
            task = TaskModel(**request_data).model_dump()

        except ValidationError as e:
            message = error_message(e)
            return json_error_response(400, description=message)

        update_result = mongo.db.tasks.update_one({"_id": ObjectId(_id)}, {"$set": task})
        if update_result.modified_count == 0:
            return json_error_response(404, description=f"Task with ID {_id} not found.")

        if (existing_book := mongo.db.tasks.find_one({"_id": ObjectId(_id)})) is not None:
            return marshal(existing_book, task_fields)

        return json_error_response(404, description=f"Task with ID {_id} not found.")


api.add_resource(TaskListAPI, "/todo/api/v1.0/tasks", endpoint="tasks")
api.add_resource(TaskAPI, "/todo/api/v1.0/tasks/<string:_id>", endpoint="task")
