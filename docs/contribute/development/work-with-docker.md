# Work with Docker

## Get the docker container id and name

Docker container ID or NAME could be obtained by `docker ps -aqf 'name=climatemind-backend_api'`. Alternatively, you can find the container name by running the `docker ps` command.

<figure><img src="../../.gitbook/assets/Screenshot 2022-11-08 at 11.20.30.png" alt=""><figcaption><p>The first column of docker ps command shows container id. The last one shows container name.</p></figcaption></figure>

## Check the docker container logs

To check docker container logs run the following [logs](https://docs.docker.com/engine/reference/commandline/logs/) command:

```
docker logs CONTAINER_ID_OR_NAME
```

`CONTAINER_ID_OR_NAME` is a container name or id which can be obtained by running the [command above](work-with-docker.md#undefined).

## Execute command in docker container

To execute a command inside the container running in the **background** use the following command:

```bash
docker exec -it CONTAINER_ID_OR_NAME COMMAND
```

* Where `COMMAND` is a command like `bash,` [pytest](unit-tests.md#pytest) or even [flask shell](https://flask.palletsprojects.com/en/2.0.x/shell/)
* `CONTAINER_ID_OR_NAME` is a container name or id which could be obtained by running the [command above](work-with-docker.md#undefined).

## Free memory

To stop containers without removing them run:

```bash
docker-compose -p climatemind-backend --profile webapp -f docker/docker-compose.yml stop
```

## Free disk space or fix issues

If you want to free some disc space and [remove](https://docs.docker.com/engine/reference/commandline/compose\_down/) containers, networks, volumes, and images created by `docker-compose -p climatemind-backend -f docker/docker-compose.yml up` run the following command.

```bash
docker-compose -p climatemind-backend -f docker/docker-compose.yml down
```

{% hint style="warning" %}
To start from scratch and **completely remove the local database** add `-v` argument to the `down` command.
{% endhint %}

You also have the option to **remove all docker data** :warning:, not only climatemind-related, but **everything** including downloaded images and build cache of any other project.&#x20;

```bash
docker system prune -a
```

## Updating frontend image

You have to update the frontend image from time to time using the following command:

```bash
docker-compose -p climatemind-backend --profile webapp -f docker/docker-compose.yml pull
```

