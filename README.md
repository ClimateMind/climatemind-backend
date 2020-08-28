# Climatemind Backend

## Using local database for development

The application is using Flyway for database migration. For development purposes we're using SQLite3. You can download an SQLite3 GUI from here: https://sqlitebrowser.org/dl/

If you want to add/modify a table or insert/delete data, you can do it with migration scripts:
 - create a new sql script in db/migration folder, starting with an uppercase 'V', increment the version and add a compact title
 - example: V2.00__create-user-table.sql, V3.00__alter_user_table.sql, V4.00__insert-test-users.sql
 
If you're using it first, or there is a new migration script (after a git pull) you must run a Flyway migrate with docker-compose:
    
    docker-compose up migration
    
Important: 
 - please don't commit your database file
 - if your database is corrupted, just delete the file and run the docker-compose script again

## Using Docker

Using Docker you need to install it first: https://www.docker.com/products/docker-desktop

On Windows it is running in a strict secure mode. You need to add the source directory to the Docker Resources: Settings / Resources / File Sharing -> add the application root directory

### Running the application with Docker Compose (for development)

Start in foreground (good for debugging flask and see the logs). You can stop it with [CTRL + C].
 
    docker-compose up web
    
Start in background

    docker-compose up -d web
    
Stop the container which is running in the background

    docker-compose down web

### Running the application with Docker (for deployment)

The Docker lifecycle is to build the image and run it only once. After that you can stop or start the image. 

Building Docker image

    docker build -t "climatemind-backend:0.1" .
    
Checking the built image

    docker images climatemind-backend
    
Running Docker

    docker run -d --name climatemind-backend --publish 5000:5000 climatemind-backend:0.1

Stop the container

    docker stop climatemind-backend
    
Start the container

    docker start climatemind-backend

