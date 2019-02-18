#!/bin/sh

if [[ "$1" == "" ]]; then
  CMD="test"
else
  CMD="$1"
fi
if [[ "$CMD" == "test" ]]; then
    echo "Running tests...."
    echo "==========================="
    python -m pytest api_jwt_tests.py
    echo "Running prospector...."
    echo "==========================="
    prospector --path=/src --profile=prospector.yml
    echo "Running sphinx build...."
    echo "==========================="
    make html
elif [[ "$CMD" == "build" ]]; then
    echo "Running sphinx build...."
    echo "==========================="
    make html
    echo "Making distro..."
    python setup.py sdist
    echo "Test releasing to pypitest repository from ./.pypirc ..."
    twine upload --repository pypitest dist/*
    echo "Done"
elif [[ "$CMD" == "release" ]]; then
    echo "Running sphinx build...."
    echo "==========================="
    make html
    echo "Making distro..."
    python setup.py sdist
    echo "Releasing to pypi repository from ./.pypirc ..."
    twine upload --repository pypi dist/*
    echo "Done"
fi

if [[ "$1" == "" ]]; then
    tail -f /dev/null
fi
