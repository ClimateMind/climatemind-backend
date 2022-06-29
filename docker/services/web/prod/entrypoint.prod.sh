#!/usr/bin/env bash

echo "sleeping entrypoint"
sleep 45

flask db upgrade

gunicorn --bind 0.0.0.0:5000 climatemind:app