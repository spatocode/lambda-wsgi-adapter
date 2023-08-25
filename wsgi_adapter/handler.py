# Copyright (c) 2023, Ekene Izukanne

import base64
from io import BytesIO
import sys
from urllib.parse import urlencode
from .response import LambdaWSGIResponse

class LambdaWSGIHandler:
    def __init__(self, wsgi_application):
        self.wsgi_application = wsgi_application

    def __call__(self, event, context):
        environ = self.create_wsgi_environment(event, context)
        response = LambdaWSGIResponse(self.wsgi_application, environ)
        return response(event)

    def create_wsgi_environment(self, event, context):
        body = event.get("body", "") or ""
        if event.get("isBase64Encoded", False):
            body = base64.b64decode(body)
        elif isinstance(body, str):
            body = body.encode("utf-8")

        environ = {
            "wsgi.url_scheme": "",
            "wsgi.version": (1, 0),
            "wsgi.multithread": False,
            "wsgi.run_once": False,
            "wsgi.multiprocess": False,
            "wsgi.errors": sys.stderr,
            "wsgi.input": BytesIO(body),
            "HTTPS": "on",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "REMOTE_ADDR": "127.0.0.1",
            "SCRIPT_NAME": "",
            "SERVER_NAME": "",
            "SERVER_PORT": "",
            "PATH_INFO": event.get("path"),
            "REQUEST_METHOD": event.get("httpMethod"),
            "QUERY_STRING": urlencode(event.get("queryStringParameters", {}) or {}),
            "CONTENT_LENGTH": str(len(body)),
            "lambda.context": context,
            "lambda.event": event
        }

        return environ
