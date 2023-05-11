#!/bin/bash

python /code/manage.py collectstatic --noinput
python manage.py migrate --noinput
exec python manage.py runserver 0.0.0.0:8000

exec "$@"