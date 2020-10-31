#!/usr/bin/env bash
#flask db init
sleep 15
/opt/mssql-tools/bin/sqlcmd -S tcp:db -U SA -P Cl1mat3m1nd! -Q "CREATE DATABASE [sqldb-web-prod-001]"

flask db migrate -m "added all tables"
flask db upgrade
flask run --host=0.0.0.0


