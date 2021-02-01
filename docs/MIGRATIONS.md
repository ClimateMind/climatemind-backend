# Migrations

When changes are made to the database structure, migrations are performed with Flask-Migrate to
update these changes within SQLalchemy.

Migrations happen in two places, locally and within the Azure Cloud. The steps to run the migrations
differ slightly between the two.

You will need to run a migration anytime the models in the models.py file are changed.

## Running A Local Migration

1. Update the relevant model
2. Open the climatemind-backend/migrations\_local/versions folder and delete the .py file inside.
3. Open the entrypoint.sh file in the climatemind-backend directory
4. Uncomment the following:
```
# flask db migrate -m "add all current tables" -d $BASEDIR/migrations_local
```

**_Make sure the $BASEDIR/migrations\_azure line IS COMMENTED OUT_**

5. Navigate to the climatemind-backend directory using the terminal/command-line. Run:

```
docker-compose down
docker-compose build
docker-compose up
```

6. Review the output in terminal/command-line and ensure the local tables have been created
7. Test the API endpoints locally to ensure the application is still working 

## Running A Cloud Migration

1. Update the relevant model
2. Open the entrypoint.sh file in the climatemind-backend directory
3. Uncomment the following:
```
# flask db migrate -m "CM-### - MESSAGE_HERE" -d $BASEDIR/migrations_azure

```
**_Make sure the $BASEDIR/migrations\_local line IS COMMENTED OUT_**

4. Comment out the following, so that upgrades are not run simultaneously.
```
if [ "$DATABASE\_PARAMS" = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;" ]
then
    flask db upgrade -d $BASEDIR/migrations_local #this line used only if local database is being used
    python add\_lrf\_table.py
else
    flask db upgrade -d $BASEDIR/migrations\_azure #this line used only if production database is being used 
    # NOTE: migrate and upgrade must be run SEPARATELY for cloud migrations. 
    # COMMENT OUT the upgrade code and run the migration first.
    # AFTER migrating, manually edit the migration script to prevent the lrf table being dropped. 
    # THEN comment out the migrate command and run upgrade.
    # ONLY run the python add\_lrf\_table script if the csv file changes.
    # python add\_lrf\_table.py
fi
```

5. Open docker-compose.yml
6. Comment out the following

```
DATABASE\_PARAMS: Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;
```

7. After this line, copy paste the DATABASE_PARAMS using the cloud db credentials from azure console (this should be uncommented so it runs)
8. Navigate to the climatemind-backend directory (locally) and run the following:

```
docker-compose down
docker-compose build
docker-compose up
```

9. In the climatemind-backend/migrations-azure/versions folder open put\_lrf\_table\_back.py
10. Remove the following code from upgrade()

```
op.drop_index("ix_lrf_data_postal_code", table_name="lrf_data")
op.drop_table("lrf_data")
```

11. Remove the following code from downgrade()

```
op.create_table(
        "lrf_data",
        sa.Column("postal_code", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column(
            "http://webprotege.stanford.edu/R9vkBr0EApzeMGfa0rJGo9G",
            mssql.BIT(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "http://webprotege.stanford.edu/RJAL6Zu9F3EHB35HCs3cYD",
            mssql.BIT(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "http://webprotege.stanford.edu/RcIHdxpjQwjr8EG8yMhEYV",
            mssql.BIT(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "http://webprotege.stanford.edu/RDudF9SBo28CKqKpRN9poYL",
            mssql.BIT(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "http://webprotege.stanford.edu/RLc1ySxaRs4HWkW4m5w2Me",
            mssql.BIT(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_index(
        "ix_lrf_data_postal_code", "lrf_data", ["postal_code"], unique=False
    )
```


10. In climatemind-backend/entrypoint.sh, Re-Comment the migrate code out and the upgrade code block back. Exclude the notes and the command to run the python add lrf script (this should only be run if the lrf data has changed and needs to be added).
11. Run the following again:

```
docker-compose down
docker-compose build
docker-compose up
```

12. In climatemind-backend/docker-compose.yml, delete the DATABASE\_PARAMS with the azure parameters and uncomment the original DATABASE\_PARAMS line.
13. Check that the cloud db has been updated
14. Test the changes

Co-written by
@seanmajorpayne @y-himanen