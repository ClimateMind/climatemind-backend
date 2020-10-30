#!/usr/bin/env bash
#flask db init
flask db migrate -m "added all tables"
flask db upgrade
flask run --host=0.0.0.0
