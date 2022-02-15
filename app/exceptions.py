from dataclasses import dataclass

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from frozendict import frozendict
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.errors import (
    MALFORMED_REQUEST_ERROR,
    MISSING_FIELD_VALUES,
    REQUEST_MAXIMUM_LENGTH_EXCEEDED,
    TYPE_VALIDATION_ERROR,
    UNKNOWN_ERROR_OCCURRED,
    TypeErrorUndefined,
)


@dataclass
class ErrorCodeMapping:
    """A dataclass that holds error code mappings to their respective status codes

    :param error_code: Error codes used to identify what error was raised and why
    :type error_code: str
    :pram tatus_code: The HTTP status code raised alongside error_code
    :type status_code: int
    """

    error_code: str
    status_code: int


ERROR_MAPPINGS: frozendict[str, ErrorCodeMapping] = frozendict(
    {
        "type_error": ErrorCodeMapping(
            TYPE_VALIDATION_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY
        ),
        "value_error.jsondecode": ErrorCodeMapping(
            MALFORMED_REQUEST_ERROR, status.HTTP_400_BAD_REQUEST
        ),
        "max_length": ErrorCodeMapping(
            REQUEST_MAXIMUM_LENGTH_EXCEEDED,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        "value_error.missing": ErrorCodeMapping(
            MISSING_FIELD_VALUES, status.HTTP_400_BAD_REQUEST
        ),
    }
)


def __get_error_type(exc: RequestValidationError) -> str:
    """Gets the error type from RequestValidationError

    :param exc: The full executed error from RequestValidationError
    :type exc: RequestValidationError
    :returns: The error type from RequestValidationError
    :rtype: str
    :raises MissingTypeErrorError: If RequestValidationError does not
    contain a key-value pair for "type"
    """

    if exc.errors()[0]["type"]:
        return exc.errors()[0]["type"]
    else:
        raise TypeErrorUndefined


def __create_exception(
    exc: RequestValidationError, status_code: int, error_code: str
) -> JSONResponse:
    """Modifies the standard RequestValidationError response to include custom status codes and error codes

    :param exc: The full executed error from RequestValidationError
    :type exc: RequestValidationError
    :param error_code: Error codes used to identify what error was raised and why
    :type error_code: str
    :pram status_code: The HTTP status code raised alongside error_code
    :type status_code: int
    :returns: A modified JSON response with custom status codes and error codes
    :rtype: JSONResponse
    """

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "detail": {
                    "error": error_code,
                    "msg": exc.errors(),
                },
            },
        ),
    )


def __create_unknown_exception(exc: RequestValidationError) -> JSONResponse:
    """Creates an exception template response for unknown exceptions raised by RequestValidationError

    :param exc: The full executed error from RequestValidationError
    :type exc: RequestValidationError
    :returns: An exception template for unknown exceptions
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": {
                    "error": UNKNOWN_ERROR_OCCURRED,
                    "msg": exc.errors(),
                },
            },
        ),
    )


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Overwrites FastAPI's RequestValidationError to return user defined error codes

    :param request: The request model that is being validated by FastAPI
    :type request: Request
    :param exc: The original RequestValidaionError message that would have been raised
    :type exc: RequestValidationError
    :returns: A json response with user defined error codes depending on the error raised
    by RequestValidationError
    :rtype: JSONResponse
    """
    unknown_exception: JSONResponse = __create_unknown_exception(exc)

    try:
        error_type: str = __get_error_type(exc)
    except TypeErrorUndefined:
        return unknown_exception

    for key, value in ERROR_MAPPINGS.items():
        if key in error_type:
            return __create_exception(exc, value.status_code, value.error_code)
    return unknown_exception
