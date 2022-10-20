ARG LOCAL_REGISTRY_URL=""
FROM ${LOCAL_REGISTRY_URL}node:12-slim AS node
FROM ${LOCAL_REGISTRY_URL}python:3.9.7-slim

COPY --from=node /usr/local /usr/local/
ENV APP_DIR /opt/app
RUN mkdir -p /usr/share/man/man1 && pip install --upgrade pip &&  apt-get update && apt-get install -y python3-dev build-essential wget curl libpq-dev default-jre-headless

WORKDIR ${APP_DIR}
COPY requirements*.txt ${APP_DIR}/
RUN pip install --target=../layers/django_requirements/python/ -r requirements-django.txt && pip install --target=../layers/boto_requirements/python/ -r requirements-boto.txt
RUN pip install -r requirements-dev.txt
 
COPY package*.json ${APP_DIR}/
RUN npm install
COPY serverless.yml ${APP_DIR}/

RUN npx sls dynamodb install --config=serverless.yml --stage=local
COPY . ${APP_DIR}/

# Set dummy credentials to run with local serverless
RUN aws configure set default.aws_secret_access_key dummy_secret_key \
    && aws configure set default.aws_access_key_id dummy_access_key_id

RUN useradd -ms /bin/bash web-api
USER web-api

