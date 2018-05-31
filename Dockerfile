FROM python:3 as python-base
MAINTAINER Hudya Admin

WORKDIR /src/
ADD api_jwt /src/api_jwt

# Cache this
RUN apt-get install libffi-dev
RUN pip install --upgrade pip \
    && pip install -U prospector cryptography pytest pyjwt
COPY prospector.yml /src/prospector.yml

RUN python -m pytest api_jwt/api_jwt_tests.py
RUN prospector --path=/src --profile=prospector.yml


FROM python:3
WORKDIR /src/
ADD . /src/

COPY .pypirc /root/.pypirc

RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT '/src/entrypoint.sh'
