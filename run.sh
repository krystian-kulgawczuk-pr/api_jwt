#!/bin/sh

if [[ "$1" == "" ]]; then
  CMD="build"
else
  CMD="$1"
fi
if [[ "$CMD" == "build" ]]; then
    echo "Running tests...."
    echo "==========================="
    python -m pytest src/api_jwt_tests.py
    echo "Running prospector...."
    echo "==========================="
    prospector --path=/src --profile=prospector.yml
    echo "Running sphinx build...."
    echo "==========================="
    make html
fi

if [[ "$1" == "" ]]; then
    tail -f /dev/null
fi
