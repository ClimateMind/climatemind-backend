# ➡ Installation

## Before you start

{% hint style="danger" %}
Please be aware of the special OS-specific cases below
{% endhint %}

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

## Installing Docker

Install [Docker](https://www.docker.com/products/docker-desktop) through their website.

{% hint style="info" %}
Before doing what's below, be sure the Docker application is running.
{% endhint %}

## Project download

Create a folder to hold the project&#x20;

```bash
mkdir climatemind && cd climatemind
```

And `git clone` [Back End](https://github.com/ClimateMind/climatemind-backend) repository into it

```bash
git clone https://github.com/ClimateMind/climatemind-backend.git
```

## Up containers

To build and up containers run the following command:

```
docker-compose -p climatemind-backend --profile webapp -f docker/docker-compose.yml up -d --build
```

It contains some optional arguments that you can omit if needed:

* `--build` can be used if the docker image will need to be re-built (e.g. adding new dependencies)
* `-d` run containers in the background is a recommended method for development which allows you to run not only the dev server but other tools like migrations, tests, etc. You could also use a[ Docker Desctop](https://www.docker.com/products/docker-desktop/) to run all containers in the background.
* `--profile webapp` to pull and run the frontend web app which will be accessible by [http://localhost:3000/](http://localhost:3000/)

## Is it work?

To check that everything is up and running go into the docker desktop and check you have three running containers under the `climatemind-backend` app.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2022-11-08 at 11.17.42.png" alt=""><figcaption><p>Docker desctop window with climate-backend running</p></figcaption></figure>

You can also do this from the command line with `docker ps`

<figure><img src="../.gitbook/assets/Screenshot 2022-11-08 at 11.20.30.png" alt=""><figcaption><p>Checking docker containers in the terminal</p></figcaption></figure>

{% hint style="warning" %}
Note that you need to wait a bit after the new containers are created.
{% endhint %}

By checking logs you can see if is it ready or not.

* In `webapp` container's log you should see `You can now view climatemind-frontend in the browser.` after compiling.
* In `api` container's log search for `Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)` after `sleeping entrypoint`

## Troubleshooting

### climatemind-backend\_api&#x20;

#### /usr/bin/env: ‘bash\r’: No such file or directory

Happens when you are on **Windows**. `climatemind-backend_db`  and `climatemind-backend_webapp` are up and running, but  `climatemind-backend_api` exits right away after the start. if by [checking docker logs](work-with-docker.md#check-the-docker-container-logs) for the container you see the following error.

```
/usr/bin/env: ‘bash\r’: No such file or directory
```

That means you forgot to take the [required preparation ](installation.md#before-you-start)step. Please remove the `climatemind-backend` folder and start from scratch.

### climatemind-backend\_webapp

#### The container unexpectedly stopped after some time

Usually happens after the first start. Try to start it again.

### climatemind-backend\_db
