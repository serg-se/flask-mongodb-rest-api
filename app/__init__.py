from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api

from config import Config

mongo = PyMongo()
api = Api(title="API", version="1.0", description="Flask-RestX API.")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    from app.main import bp as main_bp

    api.init_app(main_bp)

    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    return app
