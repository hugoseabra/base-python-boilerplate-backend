#!/usr/bin/env bash

source /code/deploy/docker/scripts/runner.sh

run_python_script "Collecting static files" "manage.py collectstatic --noinput --verbosity 0"

echo " > Initilizing SERVER"
echo ;
echo "########################################################################"
echo ;
gunicorn project.wsgi:application --bind 0.0.0.0:8000
