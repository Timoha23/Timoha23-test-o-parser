#!/bin/sh
echo "start makemigrations"
python manage.py makemigrations
echo "end amakemigrations"
echo "start migrate"
python manage.py migrate
echo "end migrate"
echo "collect static"
python manage.py collectstatic --noinput
echo "runserver"
python manage.py runserver 0.0.0.0:80 --noreload
"$@"