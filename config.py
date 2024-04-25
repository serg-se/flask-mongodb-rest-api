import os


class Config:
    MONGO_HOSTNAME = os.environ.get("MONGO_HOSTNAME") or "localhost"
    MONGO_PORT = os.environ.get("MONGO_PORT") or "27017"
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME") or "tasks_db"
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME") or "root"
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD") or "foobarbaz"
    MONGO_AUTH_SOURCE = os.environ.get("MONGO_AUTH_SOURCE") or "admin"

    MONGO_URI = (
        "mongodb://"
        + MONGO_USERNAME
        + ":"
        + MONGO_PASSWORD
        + "@"
        + MONGO_HOSTNAME
        + ":"
        + MONGO_PORT
        + "/"
        + MONGO_DBNAME
        + "?authSource="
        + MONGO_AUTH_SOURCE
    )
