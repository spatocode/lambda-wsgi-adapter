# Copyright (c) 2023, Ekene Izukanne

from io import BytesIO
import sys
import unittest
from urllib.parse import urlencode
from wsgi_adapter import LambdaWSGIHandler
from wsgi_adapter.response import LambdaWSGIResponse

class TestLambdaWSGIAdapter(unittest.TestCase):
    def compare(self, a, b, msg=None):
        if a.getvalue() != b.getvalue():
            raise self.failureException(msg)

    def test_build_headers(self):
        context = object()
        event = {
            "body": "",
            "resource": "/{proxy+}",
            "requestContext": {},
            "queryStringParameters": {},
            "headers": {
                'Host': 'wsgi_adapter.com',
                'Content-type': 'text/plain',
                'X-forwarded-for': '127.0.0.1, second',
                'X-forwarded-proto': 'https',
                'X-forwarded-port': '80',
                'X-test-suite': 'testing',
            },
            "pathParameters": {"proxy": "return/request/url"},
            "httpMethod": "GET",
            "stageVariables": {},
            "path": "/return/request/url",
        }
        expected = {
            'REQUEST_METHOD': event['httpMethod'],
            'SCRIPT_NAME': '',
            'PATH_INFO': event['path'],
            'QUERY_STRING': urlencode(event['queryStringParameters']),
            'CONTENT_LENGTH': str(len(event['body'])),
            'HTTPS': 'on',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.input': BytesIO(event['body'].encode('utf-8')),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'CONTENT_TYPE': event['headers']['Content-type'],
            'HTTP_CONTENT_TYPE': event['headers']['Content-type'],
            'SERVER_NAME': event['headers']['Host'],
            'HTTP_HOST': event['headers']['Host'],
            'REMOTE_ADDR': event['headers']['X-forwarded-for'].split(', ')[0],
            'HTTP_X_FORWARDED_FOR': event['headers']['X-forwarded-for'],
            'wsgi.url_scheme': event['headers']['X-forwarded-proto'],
            'HTTP_X_FORWARDED_PROTO': event['headers']['X-forwarded-proto'],
            'SERVER_PORT': event['headers']['X-forwarded-port'],
            'HTTP_X_FORWARDED_PORT': event['headers']['X-forwarded-port'],
            'HTTP_X_TEST_SUITE': event['headers']['X-test-suite'],
            'lambda.event': event,
            'lambda.context': context
        }
        response = LambdaWSGIResponse(object(), dict())
        environ = response.build_headers(event)
        for k, v in environ.items():
            self.assertEqual(v, expected[k])

    def test_environ(self):
        context = object()
        event = {
            "body": "",
            "resource": "/{proxy+}",
            "requestContext": {},
            "queryStringParameters": {},
            "headers": {
                'Host': 'wsgi_adapter.com',
                'Content-type': 'text/plain',
                'X-forwarded-for': '127.0.0.1, second',
                'X-forwarded-proto': 'https',
                'X-forwarded-port': '80',
                'X-test-suite': 'testing',
            },
            "pathParameters": {"proxy": "return/request/url"},
            "httpMethod": "GET",
            "stageVariables": {},
            "path": "/return/request/url",
        }
        expected = {
            'REQUEST_METHOD': event['httpMethod'],
            'SCRIPT_NAME': '',
            'PATH_INFO': event['path'],
            'QUERY_STRING': urlencode(event['queryStringParameters']),
            'CONTENT_LENGTH': str(len(event['body'])),
            'HTTPS': 'on',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.input': BytesIO(event['body'].encode('utf-8')),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'CONTENT_TYPE': event['headers']['Content-type'],
            'HTTP_CONTENT_TYPE': event['headers']['Content-type'],
            'SERVER_NAME': event['headers']['Host'],
            'HTTP_HOST': event['headers']['Host'],
            'REMOTE_ADDR': event['headers']['X-forwarded-for'].split(', ')[0],
            'HTTP_X_FORWARDED_FOR': event['headers']['X-forwarded-for'],
            'wsgi.url_scheme': event['headers']['X-forwarded-proto'],
            'HTTP_X_FORWARDED_PROTO': event['headers']['X-forwarded-proto'],
            'SERVER_PORT': event['headers']['X-forwarded-port'],
            'HTTP_X_FORWARDED_PORT': event['headers']['X-forwarded-port'],
            'HTTP_X_TEST_SUITE': event['headers']['X-test-suite'],
            'lambda.event': event,
            'lambda.context': context
        }
        handler = LambdaWSGIHandler(object())
        environ = handler.create_wsgi_environment(event, context)
        self.addTypeEqualityFunc(BytesIO, self.compare)
        for k, v in environ.items():
            if k == 'SERVER_NAME' or k == 'SERVER_PORT' or k == 'wsgi.url_scheme':
                self.assertEqual(v, '')
                continue
            self.assertEqual(v, expected[k])
