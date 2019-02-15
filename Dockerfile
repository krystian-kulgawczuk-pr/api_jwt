FROM python:alpine3.6
MAINTAINER Greger Wedel<greger@greger.io>

WORKDIR /src/
COPY . /src/

# Cache this
RUN apk update \
    && apk add --no-cache -u build-base linux-headers \
    libffi-dev libressl-dev
RUN pip install --upgrade pip pipenv

RUN pipenv install --system --dev --ignore-pipfile

COPY .pypirc /root/.pypirc

ENTRYPOINT './run.sh'
