# Climatemind Backend

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<<<<<<< HEAD

#### Table of Contents
* [Setting up your dev environment (do this first!!)](#setting-up-your-dev-environment)
    * [Installing Docker](#installing-docker)
    * [Installing Docker-compose](#installing-docker-compose)
    * [Important Docker notes for Windows](#important-docker-notes-for-windows)
* [Running the application with Docker-compose](#running-the-application-with-docker-compose)
    * [Launching in dev environment](#launching-in-dev-environment) 
    * [Launching in production environment](#launching-in-production-environment) 
* [API Documentation](#api-documentation)
*  [Processing any new Climate Mind OWL ontology file](#processing-any-new-climate-mind-OWL-ontology-file)
* [Database](#database)
* [Extra details if started the visualization script directly above.](#extra-details-if-started-the-visualization-script-directly-above)
* [Code Style](#code-style)
* [Git Style: How to Make Commits](#git-style:-how-to-make-commits)

## Setting up your dev environment

### Installing Docker

Using Docker you need to install it first: https://www.docker.com/products/docker-desktop

### Installing Docker-compose
https://docs.docker.com/compose/install/

### Important Docker notes for Windows
On Windows it is running in a strict secure mode. You need to add the source directory to the Docker Resources: Settings / Resources / File Sharing -> add the application root directory
=======
This project uses Docker. Install it through their website: https://www.docker.com/products/docker-desktop
>>>>>>> 4e5a49ea4ce0628e54436f0d9d0b852f2aea1f8e

**_Before doing what's below, be sure the Docker application is running and the command line working directory is changed to the climatemind-backend path._**

## Running the application with Docker Compose 

### Launching in dev environment

[Return to Table of Contents](#table-of-contents)

Windows users - you may experience problems with building or starting the containers if your system automatically converts Unix line endings ('\n') to DOS line endings ('\r\n'). You can prevent this from happening by running the command below. 

    git config --global core.autocrlf false

Build the image container to download and install code dependencies needed for running the app using the build command below.

**_SPECIAL NOTE_**: _Whenever the backend repo has added new dependancies in the requirements.txt file the docker image will need to be re-built by re-running the build command._

    docker-compose build

Start in foreground (good for debugging flask and see the logs). You can stop it with [CTRL + C] on OSX, Windows, and Linux.

    docker-compose up

Start in background (best for when trying to visualize the ontology)

    docker-compose up -d

Stop the container when running in the background. Stops containers and removes containers, networks, volumes, and images created by docker-compose up.

    docker-compose down

**_SPECIAL NOTE_**: _Sometimes the terminal says 'Running on http://0.0.0.0:5000' and that url does not work in the browser. If this happens, try going to "http://127.0.0.1:5000" instead._

### Launching in production environment

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

## Api documentation

<<<<<<< HEAD
[Return to Table of Contents](#table-of-contents)

[Swagger Documentation](http://localhost:5000/swagger) is available at detailing the API endpoints available and how they should be used. Whilst in development this can be for at [http://localhost:5000/swagger](http://localhost:5000/swagger).
=======
[Swagger Documentation](http://localhost:5000/swagger) is available, detailing the API endpoints and how they should be used. Whilst in development this can be found at [http://localhost:5000/swagger](http://localhost:5000/swagger).
>>>>>>> 4e5a49ea4ce0628e54436f0d9d0b852f2aea1f8e

---

## Processing a new Climate Mind OWL ontology file

[Return to Table of Contents](#table-of-contents)

Follow these instructions to process a new version of a Climate Mind ontology OWL file into files used by Climate Mind (such as Networkx pickle file, test ontology JSON, edge list output CSV, etc).

1. Download the new OWL ontology file (if haven't already) and put it in the proper place:
    * Download the OWL ontology file by going to webprotege.stanford.edu and downloading in the format 'RDF/XML'. (If you don't have access, simply email hello@climatemind.org with your webprotege username to get access). 
    * Unzip the download and go into the folder and move/copy the single ontology file to the folder in the climatemind-backend directory folder named 'PUT_NEW_OWL_FILE_IN_HERE'

2. Change the directory to be the climatemind-backend by using the following command. The part in caps should be replaced with the path to climatemind-backend on your system (for mac):

   for OSX: `cd PATH_TO_CLIMATEMIND-BACKEND`

3. Remove any pre-existing docker container, build the new docker container, and start the new container in developer mode by running the following:

    ```
        docker-compose down
        docker-compose build
        docker-compose up -d
    ```
    
4. Store the docker container id as a variable by doing:
    * FOR MAC/LINUX:
    ```
        CLIMATEMIND_ID=$(docker ps -lq)
    ```
    * FOR PC with powershell:
    ```
        $CLIMATEMIND_ID=$(docker ps -lq)
    ```

5. Process the OWL file either without the visualization app being triggered (OPTION A) or with visualization being triggered (OPTION B)

    * OPTION A. Do this option for processing the new OWL file _without_ visualizing it after it's done processing: From the climatemind-backend directory run process_new_ontology_file.py using the climatemind docker image running in the background. Note: New files will be generated and appear in the climatemind-backend directory. These files are also listed in the git.ignore file, so don't worry about them getting pushed accidentally to the git repo.

        for OSX, run this *exactly* as below:
    ```
        docker exec -it $CLIMATEMIND_ID python process_new_ontology_file.py
    ```

    * OPTION B. Do this option for processing the new OWL file _with_ visualizing it after it's done processing. Follow these instructions to visualize an OWL file using the Dash dashboard generated by the visualize.py script:  From the climatemind-backend directory run the process_new_ontology_and_visualize.py using the climatemind docker image running in the background. Note: New files will be generated and appear in the climatemind-backend directory. These files are also listed in the git.ignore file, so don't worry about them getting pushed accidentally to the git repo.

        for OSX or PC with powershell, run this *exactly* as below:
    ```
        docker exec -it $CLIMATEMIND_ID python process_new_ontology_and_visualize.py
    ```

## Database

[Return to Table of Contents](#table-of-contents)

[Flask migrate](https://flask-migrate.readthedocs.io/en/latest/) is used to handle database structure migrations. 
Whenever the data model changes, you need to manually run `flask db migrate -m "Name of migration"`
This will generate a file under `/migrations/version` which then should be checked into GIT. Whenever the API starts up, it calls `flask db upgrade`. This command will automatically apply any new migrations to the database. No manual scripts or post release commands are required!

## Extra details if the visualization script directly above was started.

[Return to Table of Contents](#table-of-contents)

6. After running step 3 OPTION B above, find the URL that appears in the terminal and go to it in your internet browser.

    Example: "Dash is running on http://127.0.0.1:8050/" appears in the terminal, so go to http://127.0.0.1:8050/ in your internet browser.


7. Use the visualization dashboard in your internet browser.

8. When done using the dashboard, close the browser and stop the script from running by going to the terminal and pressing [CTRL + C]

## Code Style
<<<<<<< HEAD

[Return to Table of Contents](#table-of-contents)

The python code is style using [Black](https://pypi.org/project/black/)
=======
The Python code style is formatted using [Black](https://pypi.org/project/black/). Black is a file formatter that converts your code to follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards. PEP 8 provides guidelines and best practices for writing Python, and is the standard style used for modern Python libraries. 

Install Black by running `pip install black`. Note: Python 3.6.0+ is required.

Cd into the climatemind-backend directory on your computer to run black commands.
>>>>>>> 4e5a49ea4ce0628e54436f0d9d0b852f2aea1f8e

Run Black locally to see which files need formatting using `python3 -m black --check ./`

<<<<<<< HEAD
You can use Black to automatically format your files using `python3 -m black ./`


## Git Style: How to Make Commits

[Return to Table of Contents](#table-of-contents)

#### 1. Fork ClimateMind's backend repository into your GitHub account

#### 2. Clone the fork to your machine

* SSH (recommended)
    
    ```git clone git@github.com:<your-github-account>/climatemind-backend.git```
    
* HTTPS (requires login for every ```git pull```) 
    
    ```git clone https://github.com/<your-github-account>/climatemind-backend.git```

#### 3. Add the climatemind/backend repository as your 'upstream' remote

 If you run ```git remote -v``` you can see all of your remote repositories. At this point, you should only see a 'fetch'/'push' for your fork. Now we'll add the original repository we forked using:

```git remote add upstream https://github.com/ClimateMind/climatemind-backend```

[source](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork)

#### 4. Sync your local copy of your fork with the 'upstream' branch

```git fetch upstream```
```git checkout main```
```get merge upstream/main```

Make sure to do this regularly, to avoid merging conflicts. When submitting your changes upstream, later.

[source](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)

#### 4. From the Fork, create a feature branch for your Jira issue

```git checkout -b CM-<Jira-issue-number>-and-short-title```

#### 5. Customize the .gitmessagetemplate for your branch's commits
    
We want to automate good practices when making commits across our various branches.

 * First, create a copy of .gitmessagetemplate and all the people that are contributing.
    * bash command: ```$ cp .gitmessagetemplate .gitmessage```
    * powershell: TODO
* Second, add it to your project's local git config
    * bash command: ```$ git config --local commit.template```
    * powershell: TODO

#### 6. Update remote repositories with your new branch + commits

fork: ```git push origin ``` 

upstream: ```git push upstream <branch-name>```
=======
Use Black to automatically format your files using `python3 -m black ./`
>>>>>>> 4e5a49ea4ce0628e54436f0d9d0b852f2aea1f8e
