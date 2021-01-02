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
# flask db migrate -m "CM-240, task CM-298, created lrf_data table from lkp_postal_nodes.csv" -d $BASEDIR/migrations_azure
# flask db migrate -m "add all current tables" -d $BASEDIR/migrations_local

# flask db upgrade -d $BASEDIR/migrations_local #this line needs to switch automatically between local and azure based on the DATABASE_PARAMS global variable. 

if [ "$DATABASE_PARAMS" = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;" ]
then
    flask db upgrade -d $BASEDIR/migrations_local #this line used only if local database is being used
    python add_lrf_table.py
else
	flask db upgrade -d $BASEDIR/migrations_azure #this line used only if production databsae is being used 
    # The line below is used ONLY when a new CSV has been added and the lrf_table needs to be updated in the cloud.
    # python add_lrf_table.py
fi
	
flask run --host=0.0.0.0
