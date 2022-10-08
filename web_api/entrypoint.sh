#!/bin/bash
dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout 45s
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
