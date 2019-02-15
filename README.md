# Python api_jwt

This repo is common library that contains helpers for hudya project.

## How to release

Make sure you have a .pypirc file at ~/ where your credentials are stored with
e.g. pypi as server reference (used below).


`
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
`

#### Do not forget to change CHANGELOG.md.
