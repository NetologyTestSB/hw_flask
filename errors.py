from flask import jsonify


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def error_handler(er: HttpError):
    response = jsonify({"status": "error", "description": er.message})
    response.status_code = er.status_code
    return response
