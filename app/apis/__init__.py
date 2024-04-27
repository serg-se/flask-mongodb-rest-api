from flask import Blueprint
from flask_restx import Api


bp = Blueprint("api", __name__)
api = Api(bp)

from app.apis import todo_namespace

api.add_namespace(todo_namespace.ns)
