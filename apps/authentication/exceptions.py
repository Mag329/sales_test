from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, InvalidToken) and response is not None:
        response.data["detail"] = "Токен недействителен или истек."

    return response