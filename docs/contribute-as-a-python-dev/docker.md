# Docker

## Installing Docker

Install [Docker](https://www.docker.com/products/docker-desktop) through their website.

{% hint style="info" %}
Before doing what's below, be sure the Docker application is running.
{% endhint %}

## Running backend

Make sure the command line working directory is changed to the climatemind-backend path.

### Special cases:

#### Windows preparation

Windows users - you may experience problems with building or starting the containers if your system automatically converts Unix line endings ('\n') to DOS line endings ('\r\n'). You can prevent this from happening by running the command below.

```
git config --global core.autocrlf false
```

#### MacOS with M1 chip

M1 chip requires a special `yml` file. Use `docker/docker-compose.m1.yml` file in the commands below.

### Up containers

Start in the foreground (good for debugging flask and seeing the logs). You can stop it with `[CTRL + C]` on OSX, Windows, and Linux:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up
```

The application should now be running on localhost. You can access it at http://127.0.0.1:5000

{% hint style="warning" %}
Sometimes the terminal says 'Running on http://0.0.0.0:5000' and that URL does not work in the browser. If this happens, try going to "http://127.0.0.1:5000" instead.
{% endhint %}

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

{% hint style="danger" %}
You will lose all the data stored in the DB
{% endhint %}

To start from scratch and completely remove the local database add `-v` argument to the `down` command.

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml down -v
```

## Running frontend

1. `cd` into the front end folder in terminal
2. run `npm run docker:dev:build` to build the development docker container (should only take about 2.5minutes and only needs to be done when new dependencies added for frontend). If have m1 mac use instead npm run `docker:dev:build:m1mac`
3. run the appropriate command below based on your machine/OS to run the container in developer mode with your project filesystem mounted (so any edits to any file in app/src folder of your project directly instantaneously sync with the running docker container):
   * mac: `npm run docker:dev:run:mac`
   * pc (must use powershell): `npm run docker:dev:run:pc`
   * linux: `npm run docker:dev:run:linux`

## Verify everything worked

### **Back end**

Go into the docker dashboard and check you have two running containers. You can also do this from the command line with `docker ps`

<figure><img src="../../.gitbook/assets/Screenshot 2020-11-16 at 21.52.03.png" alt=""><figcaption></figcaption></figure>

### Front end

Navigate to [http://localhost:3000/](http://localhost:3000/) to view the locally running version of the app

<figure><img src="../../.gitbook/assets/Screenshot 2020-11-16 at 22.05.54.png" alt=""><figcaption></figcaption></figure>
