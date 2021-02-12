# Migrations

When changes are made to the database structure, migrations are performed with Flask-Migrate to
update these changes within SQLAlchemy. Our migration scripts are auto-generated using Alembic.

Migrations happen in two places, locally and within the Azure Cloud, where our production database is hosted. The steps to run these migrations
are different. Please read the instructions carefully and contact the team if you have any questions.

You will need to run migrations any time the models in the models.py file are changed. A local migration should be completed before any changes are made in the cloud.

We have chosen our database tools to make it as easy as possible for developers to interact with the database. However, it is important to understand a little bit about what is happening in the background. 

Looking at entrypoint.sh you will see that there are two commands that are run every time a migration is done - the migrate command and the upgrade command. The migrate command is what triggers the auto-generation of the migration script. Alembic will look for any changes in the models and automatically create a migration script based on these. These changes are then applied through the upgrade command.

The project is set up so you will get an empty set of tables to work with every time the project is spun up locally, with the exception of the LRF (location relevance flag) data. The LRF table will be generated with a full set of data every time, using a separate script that is also run when the Docker container is spun up. 

The process works a little differently in the cloud, and the migrate and upgrade commands must be run separately when performing cloud migrations. We do not run the add_lrf_table.py script unless the LRF data needs to be updated. Due to this, Alembic will assume that the LRF data should be dropped and generate a migration script accordingly. The command to drop the LRF table must be deleted from the migration script before running upgrade. 

## Running a Local Migration

1. Update the relevant model
2. Open the climatemind-backend/migrations\_local/versions folder and delete the .py file inside.
3. Open the entrypoint.sh file in the climatemind-backend directory
4. Uncomment ONLY the following:

```
# flask db migrate -m "add all current tables" -d $BASEDIR/migrations_local
```

5. Navigate to the climatemind-backend directory using the terminal/command-line. Run:

```
docker-compose down
docker-compose build
docker-compose up
```

6. Review the output in terminal/command-line and ensure the local tables have been created
7. Test the API endpoints locally to ensure the application is still working 

## Running a Cloud Migration

1. Update the relevant model
2. Open the entrypoint.sh file in the climatemind-backend directory
3. If you have run a local migration, comment out:

```
flask db migrate -m "add all current tables" -d $BASEDIR/migrations_local
```

4. Uncomment ONLY the following and change the message to reflect the changes being made:

```
# flask db migrate -m "CM-### - MESSAGE_HERE" -d $BASEDIR/migrations_azure

```

5. Comment out the following block of code, so that upgrades are not run simultaneously.

```
if [ "$DATABASE_PARAMS" = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;" ]
then
    flask db upgrade -d $BASEDIR/migrations_local #this line used only if local database is being used
    python add_lrf_table.py
else
    flask db upgrade -d $BASEDIR/migrations_azure #this line used only if production database is being used 
fi
```

6. Open docker-compose.yml
7. Comment out the following:

```
DATABASE_PARAMS: Driver={ODBC Driver 17 for SQL Server};Server=tcp:db,1433;Database=sqldb-web-prod-001;Uid=sa;Pwd=Cl1mat3m1nd!;Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;
```
8. Comment in the following:

```
DATABASE_PARAMS: ${CLOUD_DB_PARAMS}
```

9. The command above means that the CLOUD_DB_PARAMS variable needs to be set. Create an un-named .env file in the root directory of the project (where the docker-compose.yml is) and add the cloud db parameters as shown below. This file is gitignored and will/should NOT be pushed to the repository. The credentials can be found through the Azure portal (contact a member of the core team).
    
    ```
    CLOUD_DB_PARAMS=put_the_real_cloud_db_params_here_with_no_spaces_before__or_after_the_equals_sign_and_no_quotation_marks
    ```

10. Navigate to the climatemind-backend directory (locally) and run the following:

```
docker-compose down
docker-compose build
docker-compose up
```

11. In the climatemind-backend/migrations-azure/versions folder you will see a new migration script has been generated. Open this script. 
Do NOT delete or edit any other scripts in this folder (it is important to preserve the history).
12. Check that the changes you are making are correct in the script, and remove the following code from upgrade():

```
op.drop_index("ix_lrf_data_postal_code", table_name="lrf_data")
op.drop_table("lrf_data")
```

13. Remove the following code from downgrade():

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

14. In climatemind-backend/entrypoint.sh, re-comment the migrate code out and the upgrade code block back in. 
15. Run the following again:

```
docker-compose down
docker-compose build
docker-compose up
```

16. In climatemind-backend/docker-compose.yml, comment out the DATABASE_PARAMS with the cloud parameters and uncomment the original DATABASE_PARAMS line to put the local credentials back in.
17. Check that the cloud db has been updated
18. Test the changes before pushing to GitHub.

Co-written by
@seanmajorpayne @y-himanen