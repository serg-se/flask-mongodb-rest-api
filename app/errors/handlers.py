from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

from app.errors import bp


def json_error_response(status_code: int, description: any = None) -> tuple[dict[str, any], int]:
    """
    Append a short name to the given HTTP status code and return them in a format ready
    to be converted to JSON.

    Return format example:
        {"error": "Not Found", "description": "The requested URL was not found on the server."}, 404
    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if description:
        payload["description"] = description
    return payload, status_code


@bp.app_errorhandler(HTTPException)
def handle_exception(e):
    return json_error_response(e.code, e.description)
