#!/usr/bin/env bash

sleep 30 # let database spin up
flask db upgrade
flask run --host=0.0.0.0
