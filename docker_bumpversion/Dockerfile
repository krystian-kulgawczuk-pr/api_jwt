FROM python:alpine
RUN apk update && \
    apk add git && \
    pip install bumpversion

WORKDIR /etc/bump
COPY . /etc/bump
RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
CMD ["minor"]