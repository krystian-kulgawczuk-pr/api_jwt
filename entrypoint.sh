#!/bin/sh

cd /src/

echo "Testing registration on pypi and check healthcheck pypi repository"
python setup.py register -r python-hudya

echo "Uploading to pypi repository"
python setup.py sdist --format=zip upload -r python-hudya
