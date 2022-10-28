# Installation

## Installation

Create a folder to hold the project and git `git clone` [Back End](https://github.com/ClimateMind/climatemind-backend) Repos into it.

```bash
mkdir climatemind && cd climatemind
git clone https://github.com/ClimateMind/climatemind-backend.git
```

## Docker

### Installing Docker

Install [Docker](https://www.docker.com/products/docker-desktop) through their website.

{% hint style="info" %}
Before doing what's below, be sure the Docker application is running.
{% endhint %}

### Special cases:

<details>

<summary>Windows preparation</summary>

Windows users may experience problems with building or starting the containers if your system automatically converts Unix line endings ('\n') to DOS line endings ('\r\n'). You can prevent this from happening by running the command below.

```bash
git config --global core.autocrlf false
```

</details>

<details>

<summary>MacOS with M1 chip</summary>

M1 chip requires a special \`yml\` file. Use \`docker/docker-compose.m1.yml\` file in the commands below.

</details>

### Up containers

To build and up containers run the following command:

```
docker-compose -p climatemind-backend --profile webapp -f docker/docker-compose.yml up -d --build
```

It contains some optional arguments which you can omit if needed:

* `--build` can be used if the docker image will need to be re-built (e.g. adding new dependencies)
* `-d` run containers in the background is a recommended method for development which allows you to run not only the dev server but other tools like migrations, tests, etc. You could also use a[ Docker Desctop](https://www.docker.com/products/docker-desktop/) to run all containers in the background.
* `--profile webapp` to pull and run frontend web app which will be accessible by http://localhost:3000/

### Execute command in docker container

To execute a command inside the container running in the **background** use the following command:

```bash
docker exec -it CONTAINER_ID COMMAND
```

* Where `COMMAND` is a command like `bash,` [pytest](development/unit-tests.md#pytest) or even [flask shell](https://flask.palletsprojects.com/en/2.0.x/shell/)
* `CONTAINER_ID` is a container id which could be obtained by `docker ps -aqf 'name=climatemind-backend_web'`. Alternatively, you can use container name like `climatemind-backend_web_1`

### Removing containers and data

When you're done working, stop the container. Stopping containers will remove containers, networks, volumes, and images created by `docker-compose -p climatemind-backend -f docker/docker-compose.yml up`.

```bash
docker-compose -p climatemind-backend -f docker/docker-compose.yml down
```

To start from scratch and **completely remove the local database** add `-v` argument to the `down` command.

### Updating frontend image

You have to update frontend image from time to time using the following command:

```bash
docker-compose -p climatemind-backend --profile webapp -f docker/docker-compose.m1.yml pull
```

### Verify everything worked

Go into the docker dashboard and check you have three running containers under `climatemind-backend` app. You can also do this from the command line with `docker ps`

Note that you need to wait a bit after the new containers created. By checking logs you can see is it ready or not.&#x20;

* In \`webapp\` container's log you should see \`You can now view climatemind-frontend in the browser.\` after a compiling.&#x20;
* In \`api\` container's log search for \`Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)\` after \`sleeping entrypoint\`
