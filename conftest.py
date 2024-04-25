import pytest

from app import create_app, mongo
from config import Config


class TestsConfig(Config):
    TESTING = True
    MONGO_DBNAME = "test_db"

    MONGO_URI = (
        "mongodb://"
        + Config.MONGO_USERNAME
        + ":"
        + Config.MONGO_PASSWORD
        + "@"
        + Config.MONGO_HOSTNAME
        + ":"
        + Config.MONGO_PORT
        + "/"
        + MONGO_DBNAME
        + "?authSource="
        + Config.MONGO_AUTH_SOURCE
    )


@pytest.fixture(autouse=True)
def mongo_teardown():
    yield
    mongo.db.drop_collection("tasks")
    mongo.db.command("dropDatabase")


@pytest.fixture(scope="session")
def flask_client():

    app = create_app(TestsConfig)
    app_context = app.app_context()
    app_context.push()
    client = app.test_client()

    yield client
