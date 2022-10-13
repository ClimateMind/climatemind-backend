# Docker

## Installing Docker

Install [Docker](https://www.docker.com/products/docker-desktop) through their website.

## Running the application

_**Before doing what's below, be sure the Docker application is running and the command line working directory is changed to the climatemind-backend path.**_

### Special cases:

#### Windows preparation

Windows users - you may experience problems with building or starting the containers if your system automatically converts Unix line endings ('\n') to DOS line endings ('\r\n'). You can prevent this from happening by running the command below.

```
git config --global core.autocrlf false
```

#### MacOS with M1 chip

M1 chip requires a special `yml` file. Use `docker/docker-compose.m1.yml` file in the commands below.

### Up containers

Start in the foreground (good for debugging flask and seeing the logs). You can stop it with \[CTRL + C] on OSX, Windows, and Linux:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up
```

The application should now be running on localhost. You can access it at http://127.0.0.1:5000

_**SPECIAL NOTE**_: _Sometimes the terminal says 'Running on http://0.0.0.0:5000' and that url does not work in the browser. If this happens, try going to "http://127.0.0.1:5000" instead._

#### Rebuild images

Whenever the backend repo has added new dependencies in the `requirements.*` files the docker image will need to be re-built. You can do this by adding `--build` argument to the `up` command:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up --build
```

#### Start in background

Best for when trying to attach the docker instance to the front-end application. Add `-d` argument to the `up` command:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up -d
```

### Stopping containers

When you're done working, stop the container. Stopping containers will remove containers, networks, volumes, and images created by `docker-compose -p climatemind-backend -f docker/docker-compose.yml up`.

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml down
```

#### Removing local database

To start from scratch and completely remove the local database add `-v` argument to the `down` command.

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml down -v
```
