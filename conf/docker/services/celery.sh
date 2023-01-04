#!/usr/bin/env bash

source /code/deploy/scripts/runner.sh

# Define settings
export DJANGO_SETTINGS_MODULE=WiseLoanDjango.settings

run_python_script "Validating config: DB" "/code/deploy/validators/db_credentials.py"
run_python_script "Validating config: SENTRY" "/code/deploy/validators/sentry_config.py"
run_python_script "Validating config: REDIS" "/code/deploy/validators/redis_credentials.py"

echo " > Iniciando CELERY"
echo ;
echo "########################################################################"
echo ;
celery -A project worker --autoscale=10,5 -l INFO
