# DB Migrations
## Preparation
After you modified `models.py` and added or modified some models you have to prepare DB migrations as well. Follow this guide to prepare DB migration.

## Create Migration

Build docker images and up containers: 

```bash
docker-compose -p climatemind-backend -f docker/docker-compose.yml up --build -d
```

Run bash in the docker container:

```bash
docker exec -it `docker ps -aqf "name=climatemind-backend_web"` bash
```

Create migrations with `flask` command:

```bash
flask db migrate -m "#TICKET - description" 
```

## Edit migration

Open the migration file using path from the `flask db migrate` command output.
Check and modify `upgrade` and `downgrade` functions if needed.

## Apply migration

### Locally

To apply the migration run the following `flask` command inside the docker container:

```bash
flask db upgrade
```

The second option to apply the migration is to rebuild the `climatemind-backend_web` image.

### On test and prod databases

The migration will be applied automatically after deployment. 




