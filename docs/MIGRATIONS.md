# Migrations

When changes are made to the database structure, migrations are performed with Flask-Migrate to
update these changes within SQLalchemy.

TODO: @y-himanen needs to update this to the current process.

## Database
[Flask migrate](https://flask-migrate.readthedocs.io/en/latest/) is used to handle database structure migrations. 
Whenever the data model changes, you need to manually run `flask db migrate -m "Name of migration"`
This will generate a file under `/migrations/version` which then should be checked into GIT. Whenever the API starts up, it calls `flask db upgrade`. 
This command will automatically apply any new migrations to the database. No manual scripts or post release commands are required!