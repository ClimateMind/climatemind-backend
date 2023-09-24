# ➡ Installation

## Before you start

{% hint style="danger" %}
Please be aware of the special OS-specific cases below
{% endhint %}

{% tabs %}
{% tab title="Mac with Apple silicon " %}
M1 chip requires a special `yml` file. Use `docker/docker-compose.m1.yml` file in the commands below.
{% endtab %}

{% tab title="Windows" %}
Windows users may experience problems with building or starting the containers if your system automatically converts Unix line endings ('\n') to DOS line endings ('\r\n'). You can prevent this from happening by running the command below.

```bash
git config --global core.autocrlf false
```
{% endtab %}
{% endtabs %}

## Installing Docker

Install [Docker](https://www.docker.com/products/docker-desktop) through their website.

{% hint style="info" %}
Before doing what's below, be sure the Docker daemon is [running](https://docs.docker.com/config/daemon/#check-whether-docker-is-running).
{% endhint %}

## Project download

To allow everyone to participate in project development we accept changes from external [forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks). To start working, do the following steps:&#x20;

1. create a [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of the [climatemind-backend](https://github.com/ClimateMind/climatemind-backend) repository
2. [clone your fork ](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository)to your local machine

{% hint style="success" %}
[GitHub Desktop](https://desktop.github.com/) allows you to do both [fork & clone](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop#forking-a-repository) at the same time.&#x20;
{% endhint %}

## Up containers

To build and up containers open the terminal and go to the folder containing your cloned repository. Then run the following command:

{% hint style="info" %}
You may need to enable Compose V1/V2 compatibility in Docker Desktop Settings->General if your system reports the "docker-compose" command is not found. Another solution is using "docker compose" instead.
{% endhint %}

```
docker-compose -p climatemind-backend --profile webapp -f docker/docker-compose.yml up -d --build
```

It contains some optional arguments that you can omit if needed:

* `--build` can be used if the docker image will need to be re-built (e.g. adding new dependencies)
* `-d` run containers in the background is a recommended method for development which allows you to run not only the dev server but other tools like migrations, tests, etc. You could also use a [Docker Desktop](https://www.docker.com/products/docker-desktop/) to run all containers in the background.
* `--profile webapp` to pull and run the frontend web app which will be accessible by [http://localhost:3000/](http://localhost:3000/)

## Is it working?

To check that everything is up and running go into Docker Desktop and check you have three running containers under the `climatemind-backend` app.&#x20;

<figure><img src="../.gitbook/assets/Screenshot 2022-11-08 at 11.17.42.png" alt=""><figcaption><p>Docker Desktop window with climatemind-backend running</p></figcaption></figure>

You can also do this from the command line with `docker ps`

<figure><img src="../.gitbook/assets/Screenshot 2022-11-08 at 11.20.30.png" alt=""><figcaption><p>Checking docker containers in the terminal</p></figcaption></figure>

{% hint style="warning" %}
Note that you need to wait a bit after the new containers are created.
{% endhint %}

By checking logs you can see if it is ready.

* In `webapp` container's log you should see `You can now view climatemind-frontend in the browser.` after compiling.
* In `api` container's log search for `Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)` after `sleeping entrypoint`

After this, you are finally able to test the app manually on your local environment. See the following page for more details:

{% content-ref url="development/manual-testing.md" %}
[manual-testing.md](development/manual-testing.md)
{% endcontent-ref %}

## Troubleshooting

### climatemind-backend\_api&#x20;

#### ERROR: for api  Cannot start service api: Ports are not available: listen tcp 0.0.0.0:5000: bind: address already in use

Happens when port 5000 is already in use. Usually occurs with macs because they now devote port 5000 for airplay receiver. To deactivate this setting and free up port 5000, do the following: 
System Settings -> General -> uncheck ‘AirPlay Receiver’

#### /usr/bin/env: ‘bash\r’: No such file or directory

Happens when you are on **Windows**. `climatemind-backend_db`  and `climatemind-backend_webapp` are up and running, but  `climatemind-backend_api` exits right away after the start. if by [checking docker logs](development/work-with-docker.md#check-the-docker-container-logs) for the container you see the following error.

```
/usr/bin/env: ‘bash\r’: No such file or directory
```

That means you forgot to take the [required preparation ](installation.md#before-you-start)step. Please remove the `climatemind-backend` folder and start from scratch.

### climatemind-backend\_webapp

#### The container unexpectedly stopped after some time

Usually happens after the first start. Try to start it again.

### climatemind-backend\_db
