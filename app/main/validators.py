from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel, StringConstraints, ValidationError
from pydantic.functional_validators import AfterValidator
from pydantic_core import ErrorDetails, PydanticCustomError


def is_not_empty(v: str):
    if not len(v) >= 1:
        raise PydanticCustomError(
            "empty",
            "Should not be empty",
        )
    return v


TitleString = Annotated[
    str,
    StringConstraints(max_length=20),
    AfterValidator(is_not_empty),
]


DescriptionString = Annotated[
    str,
    StringConstraints(max_length=20),
]


def id_is_valid(v: str):
    if not ObjectId.is_valid(v):
        raise PydanticCustomError(
            "invalid_object_id",
            "Is not a valid ObjectId, it must be a 24-character hex string",
        )
    return v


IDString = Annotated[
    str,
    AfterValidator(id_is_valid),
]


class TaskIDModel(BaseModel):
    id: IDString


class TaskModel(BaseModel):
    title: TitleString
    description: DescriptionString = ""
    done: bool = False


CUSTOM_MESSAGES = {
    "string_too_long": "Cannot be longer then {max_length} characters",
    "string_too_short": "Cannot be shorter then {min_length} characters",
}


def converted_errors(e: ValidationError, custom_messages: dict[str, str]) -> list[ErrorDetails]:
    new_errors: list[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error["type"])
        if custom_message:
            ctx = error.get("ctx")
            error["msg"] = custom_message.format(**ctx) if ctx else custom_message
        new_errors.append(error)
    return new_errors


def error_message(e: ValidationError) -> str:
    errors = converted_errors(e, CUSTOM_MESSAGES)
    message = f"{errors[0]['msg']}."
    return message
