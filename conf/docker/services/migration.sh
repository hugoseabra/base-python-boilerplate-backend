#!/usr/bin/env bash

source /code/deploy/docker/scripts/runner.sh

run_python_script_with_output "Executando migrate" "manage.py migrate"
run_python_script_with_output "Criado tabelas de cache" "manage.py createcachetable"
