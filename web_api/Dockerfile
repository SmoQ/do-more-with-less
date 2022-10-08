FROM python:3.10.7-slim

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /opt/app

ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}/"

RUN pip install --upgrade pip && apt-get update && apt-get install -y python3-dev build-essential wget curl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR ${APP_DIR}

COPY requirements*.txt ${APP_DIR}/

RUN pip install -r requirements.txt
RUN useradd -ms /bin/bash web-api
# Set dummy credentials to run with local serverless
RUN aws configure set default.aws_secret_access_key dummy_secret_key \
    && aws configure set default.aws_access_key_id dummy_access_key_id

USER web-api

COPY . ${APP_DIR}/
