# lambda-wsgi-adapter  ![version](https://img.shields.io/pypi/v/lambda-wsgi-adapter) ![downloads](https://img.shields.io/pypi/dm/lambda-wsgi-adapter) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![issues](https://img.shields.io/github/issues/spatocode/lambda-wsgi-adapter)

WSGI adapter for AWS Lambda


## Install

```
$ pip install lambda-wsgi-adapter
```


## Usage

```py
from wsgi_adapter import LambdaWSGIHandler
from django_project.wsgi import application

def lambda_handler(event, context):
    handler = LambdaWSGIHandler(application)
    return handler(event, context)
```


# License

[MIT License](http://www.github.com/spatocode/lambda-wsgi-adapter/blob/master/LICENSE)

Copyright (c) 2023 Ekene Izukanne
