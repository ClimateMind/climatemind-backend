#!/usr/bin/env bash

echo "sleeping entrypoint"
sleep 45

BASEDIR="$(dirname "${BASH_SOURCE[0]}")"

flask db upgrade -d $BASEDIR/migrations

gunicorn --bind 0.0.0.0:5000 climatemind:app