from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import Response, exception_handler


def success_response(status, data):
    Response.status_code = status
    msg = {"success": True, "data": data}
    return Response(msg)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = error_response(exc.args)
        return response.data
    elif isinstance(exc, IntegrityError):
        response = error_response(str(exc).strip("\n").split("DETAIL:  ")[-1])
    elif isinstance(exc, ValueError) or isinstance(exc, ObjectDoesNotExist):
        response = error_response(str(exc))
    elif isinstance(exc, KeyError):
        response = error_response("Invalid Parameters")

    return response


def error_response(error_msg):
    return Response(
        {"success": False, "error": error_msg},
        status=status.HTTP_400_BAD_REQUEST,
    )
