#!/usr/bin/env bash
#wait for database to start
#sleep 15

flask db upgrade
flask run --host=0.0.0.0