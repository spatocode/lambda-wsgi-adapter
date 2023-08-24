# Copyright (c) 2023, Ekene Izukanne

from werkzeug.wrappers import Response

class LambdaWSGIResponse():
    def __init__(self, wsgi_application, environ) -> None:
        self.wsgi_application = wsgi_application
        self.environ = environ

    def __call__(self, event):
        headers = self.build_headers(event)
        self.environ.update(headers)
        with Response.from_app(self.wsgi_application, self.environ) as response:
            return self._build_response(event, response)

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
