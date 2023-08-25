#!/usr/bin/env python
# Copyright (c) 2023, Ekene Izukanne

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="lambda-wsgi-adapter",
    version="0.1.1",
    author="Ekene Izukanne",
    author_email="ekeneizukanne@gmail.com",
    description="WSGI adapter for AWS Lambda",
    license = "MIT",
    keywords='wsgi aws lambda api gateway',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spatocode/lambda-wsgi-adapter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)