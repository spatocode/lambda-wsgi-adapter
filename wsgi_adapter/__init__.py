import base64
from io import BytesIO
import sys
from urllib.parse import urlencode
from werkzeug.wrappers import Response


class AWSGIResponse():
    def build_headers(self, event):
        environ = dict()
        headers = event.get("headers", {})
        for header in headers:
            wsgi_name = "HTTP_" + header.upper().replace("-", "_")
            environ[wsgi_name] = str(headers[header])

            if headers.get("Content-Type"):
                environ["CONTENT_TYPE"] = headers["Content-Type"]

            if headers.get("Host"):
                environ["SERVER_NAME"] = headers["Host"]

            if headers.get("X-Forwarded-Proto"):
                environ["wsgi.url_scheme"] = headers["X-Forwarded-Proto"]

            if headers.get("X-Forwarded-Port"):
                environ["SERVER_PORT"] = headers["X-Forwarded-Port"]

            if headers.get("X-Forwarded-For"):
                environ["REMOTE_ADDR"] = headers["X-Forwarded-For"]
        return environ

    def create_wsgi_environment(self, event, context):
        headers = self.build_headers(event)
        body = event.get("body")
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
            "QUERY_STRING": urlencode(event.get("queryStringParameters")),
            "CONTENT_LENGTH": str(len(body)),
            "lambda.context": context,
            "lambda.event": event
        }

        environ.update(headers)
        return environ

    def _build_response(self, event, response):
        resp = dict()
        if event.get("multiValueHeaders"):
            mHeaders = dict()
            for k, v in response.headers:
                mHeaders[k] = response.headers.getlist(k)
            resp["multiValueHeaders"] = mHeaders
        if response.data:
            resp["body"] = response.get_data(as_text=True)
        if event.get("headers"):
            headers = dict()
            for k, v in response.headers:
                headers[k] = v
            resp["headers"] = headers
        resp["statusCode"] = response.status_code
        return resp

    def handler(self, application, event, context):
        environ = self.create_wsgi_environment(event, context)
        with Response.from_app(application, environ) as response:
            return self._build_response(event, response)


def response(application, event, context):
    return AWSGIResponse().handler(application, event, context)
