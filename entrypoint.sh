#!/usr/bin/env bash

echo "sleeping entrypoint"
sleep 45

BASEDIR="$(dirname "${BASH_SOURCE[0]}")"
# flask db history -d $BASEDIR/migrations --verbose
# flask db downgrade -d $BASEDIR/migrations
# flask db stamp -d $BASEDIR/migrations 04f4c14bd4af
# flask db upgrade -d $BASEDIR/migrations
# flask db init -d $BASEDIR/migrations_local
# flask db init -d $BASEDIR/migrations_azure
# flask db init -d $BASEDIR/migrations_test_db

flask db migrate -m "add all current tables" -d $BASEDIR/migrations_local
# flask db migrate -m "CM-791 session id updates" -d $BASEDIR/migrations_azure
# flask db migrate -m "CM-768 remove all relationships from tables" -d $BASEDIR/migrations_test_db

if [ "$DATABASE_PARAMS" = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;" ]
then
    flask db upgrade -d $BASEDIR/migrations_local #this line used only if local database is being used
    python add_lrf_table.py
else
    flask db upgrade -d $BASEDIR/migrations_test_db #this line used only if cloud test db is being used
    # flask db upgrade -d $BASEDIR/migrations_azure #this line used only if production database is being used
fi

flask run --host=0.0.0.0

# NOTE: migrate and upgrade must be run SEPARATELY for cloud migrations.
# COMMENT OUT the upgrade code and run the migrate command first.
# AFTER migrating, manually edit the migration script to prevent the lrf table being dropped.
# THEN comment out the migrate command and run upgrade.
# IF the CSV file changes and the lrf table needs to be updated in the cloud, add:
# python add_lrf_table.py   underneath   flask db upgrade -d $BASEDIR/migrations_azure
