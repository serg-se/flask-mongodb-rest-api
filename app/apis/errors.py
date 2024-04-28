from flask_restx import Namespace
from werkzeug.http import HTTP_STATUS_CODES


def abort_descriptive(namespace: Namespace, status_code: int, description: any = None):
    """
    Abort request with a given status code, add a short error name and a description to payload.

    Payload example:
        {"error": "Not Found", "description": "The requested URL was not found on the server."}
    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if description:
        payload["description"] = description
    namespace.abort(status_code, **payload)
