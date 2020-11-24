#!/usr/bin/env bash

echo "sleeping entrypoint"
sleep 45

BASEDIR="$(dirname "${BASH_SOURCE[0]}")"
flask db upgrade -d $BASEDIR/migrations
flask run --host=0.0.0.0
