#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 "$POSTGRES_DB" --username "$POSTGRES_USER" <<-EOSQL
CREATE EXTENSION unaccent;
EOSQL