FROM python:3 as python-base
MAINTAINER Hudya Admin

WORKDIR /src/
COPY . /src/

# Cache this
RUN apt-get install libffi-dev
RUN pip install --upgrade pip \
    && pip install -U prospector cryptography pytest pyjwt

RUN python -m pytest api_jwt_tests.py
RUN prospector --path=/src --profile=prospector.yml

RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT '/src/entrypoint.sh'
