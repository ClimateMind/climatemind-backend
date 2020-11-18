#!/usr/bin/env bash

echo "sleeping entrypoint"
sleep 30

#flask db upgrade
flask run --host=0.0.0.0