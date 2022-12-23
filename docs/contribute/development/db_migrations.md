# DB Migrations

## Preparation

After you have edited `models.py` and added or modified some models, you have to prepare DB migrations as well. Follow this guide to prepare DB migration.

## Create migration

Build docker images and up containers:

```bash
docker-compose -p climatemind-backend -f docker/docker-compose.yml up --build -d
```

Wait for app and database startup to finish, then run bash in the docker container:

```bash
docker exec -it `docker ps -aqf "name=climatemind-backend_web"` bash
```

Create migrations with `flask` command:

```bash
flask db migrate -m "#TICKET - description" 
```

## Edit migration

Open the migration file using the path given by the `flask db migrate` command. Check and modify `upgrade` and `downgrade` functions if needed.

## Apply migration

### Locally

To apply the migration run the following `flask` command inside the docker container:

```bash
flask db upgrade
```

Alternatively, the migration can be applied by rebuilding the `climatemind-backend_web` image.

#### Remove local database

To remove the local database and start from scratch you can use `docker-compose down` with `-v` argument to remove volumes

```bash
docker-compose -p climatemind-backend -f docker/docker-compose.yml down -v
```

### On test and prod databases

The migration will be applied automatically after deployment.
