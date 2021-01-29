# Climatemind Backend

![[Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Code-Flask-informational?style=flat&logo=flask&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Tools-Docker-informational?style=flat&logo=docker&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Server-Azure-informational?style=flat&logo=microsoftazure&logoColor=white&color=2bbc8a)

The [Climate Mind application](https://app.climatemind.org) makes conversations about climate change easier, by letting users explore climate issues
that speak to their personal values. We aim to inspire users to take action with a range of attractive solutions consistent 
with their values that they can get excited about.

The application currently presents solutions based on their personal values (as determined by a questionnaire) and their location (zip code).
In the future, we plan to add the user's occupation as an option to personalize the results.

## An Overview of How this Works

In order to serve users with relevant climate information our data team has organized climate data into an Ontology. Don't let
the fancy term overwhelm you, as it is (at the end of the day) a data structure. It contains information about the relationships between climate issues, solutions,
myths, and other data.

However, this data structure, in it's native form, is not easy to work with. We have another repo [climatemind-ontology-processing](https://github.com/ClimateMind/climatemind-ontology-processing)
which does all of the hard work to convert this data into an easy to work with graph structure (known as NetworkX). This graph is packaged into the .gpickle file
found in the /output directory and read by the application.

Detailed instructions for processing the ontology can be found [below](#owl-file-processing) or in the [climatemind-ontology-processing repo](https://github.com/ClimateMind/climatemind-ontology-processing)

In order to use this application there are three steps

1. Install the project and install Docker
2. Install the Ontology Processing repo through Pip
2. Download the Ontology file and process it to create the .gpickle
3. Build the application with Docker
3. Launch the application with Docker

Following are more details about each of these steps

## Installing the Project

To intall the code to your local machine, navigate to the desired parent folder via the command line and clone the repo

```
git clone https://github.com/ClimateMind/climatemind-backend.git
```

You will now have access to our backend code.

Next install [Docker](https://www.docker.com/products/docker-desktop) through their website.

## Install the Ontology Processing Repo

**_Be sure git is installed on your computer before installing the repo_**

Open up your command prompt/terminal and install the package as follows:

Be sure you have installed all requirements first by doing:

```
python3 -m pip install -r https://raw.githubusercontent.com/ClimateMind/climatemind-ontology-processing/main/requirements.txt
```

Then, install the package via pip install:

```
python3 -m pip install git+https://github.com/ClimateMind/climatemind-ontology-processing.git
```

**_Before doing what's below, be sure the Docker application is running and the command line working directory is changed to the climatemind-backend path._**

## Running the application with Docker Compose (for development)

Windows users - you may experience problems with building or starting the containers if your system automatically converts Unix line endings ('\n') to DOS line endings ('\r\n'). You can prevent this from happening by running the command below. 

    git config --global core.autocrlf false

Build the image container to download and install code dependencies needed for running the app using the build command below.

**_SPECIAL NOTE_**: _Whenever the backend repo has added new dependancies in the requirements.txt file the docker image will need to be re-built by re-running the build command._

    docker-compose build

Start in foreground (good for debugging flask and see the logs). You can stop it with [CTRL + C] on OSX, Windows, and Linux.

    docker-compose up

Start in background (best for when trying to visualize the ontology or when attaching the docker instance to the front-end application)

    docker-compose up -d

When you're done working, stop the container when running in the background. Stopping containers will remove containers, networks, volumes, and images created by docker-compose up.

    docker-compose down

**_SPECIAL NOTE_**: _Sometimes the terminal says 'Running on http://0.0.0.0:5000' and that url does not work in the browser. If this happens, try going to "http://127.0.0.1:5000" instead._

## Running the application with Docker (for deployment)

The Docker lifecycle is to build the image and run it only once. After that you can stop or start the image.
**_If you are a new developer on the team, you do not need to do this_**

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

[AutoDoc](http://localhost:5000/documentation) Our API is currently documented using AutoDoc. This will soon be deprecated and replaced with Swagger. 

[Swagger Documentation](http://localhost:5000/swagger) will be available soon, detailing the API endpoints and how they should be used. Whilst in development this can be found at [http://localhost:5000/swagger](http://localhost:5000/swagger).

---

## OWL File Processing

Climatemind uses an ontology to store climate change data and relationships. This data
is stored as an RDF/XML file and is not easily worked with in Python.

We need to convert this file to a NetworkX object and save it as a Pickle file so it is
easier to work with. Luckily, since we've already written the code for this, we've made
this process relatively simple. Our code is available as a Pip install.

Complete the following instructions to process the OWL file.

### Do this your first time

Be sure git is installed on your computer first. Open up your command prompt/terminal and
install the package as follows:

Install the package via pip install:

```
python3 -m pip install git+https://github.com/ClimateMind/climatemind-ontology-processing.git
```

Be sure you have installed all requirements first by doing:

```
python3 -m pip install -r https://raw.githubusercontent.com/ClimateMind/climatemind-ontology-processing/main/requirements.txt
```

Now you're all set up and ready to roll!

### Do this every time

1. Download a fresh copy of the ontology from web protege. Make sure it's the RDF/XML format (check the downloaded item has .owl at the end of it!).
2. Put the .owl file into the PUT\_NEW\_OWL\_FILE\_IN\_HERE folder
3. Using the terminal/command-line, navigate to the climatemind-backend/process\_ontology folder.
4. Run the process.py script by executing the following

```
python3 process.py
```

Ensure that you are in the process\_ontology folder when you run this or the command will not
find the file.

5. Check the climatemind-backend/gpickle folder. If you did this correctly, there should be a .pickle file.
6. You can now run the app and it will automatically use this gpickle file.

## Backend Debugging

We use pdb to debug and troubleshoot issues. You can run pdb a few ways. First you need to set a breakpoint() in the code where you want to stop and examine the state of variables.

Then run one of the following for scripts:
```
# For Scripts (eg. process_new_ontology_file.py):
# Note that this is only for scripts that have to be run
docker exec -it $CLIMATEMIND_ID python process_new_ontology_file.py
```

Or the following for the general docker instance:
```
# Run the docker instance in the background and attach to the docker image
docker-compose up -d
docker attach climatemindproduct_web_1
# Navigate to the frontend directory in a separate terminal
cd climatemind-frontend

# If desired, you can link the local frontend app and test (you can also just use
#postman and breakpoints will still happen)
# First time only - Install npm
npm -i
# Start the local frontend server with npm
npm start
```

Now you will have breakpoints in the docker container that you can interact with. Learn more about what
you can do in the [pdb documentation](https://docs.python.org/3/library/pdb.html)

## Database
[Flask migrate](https://flask-migrate.readthedocs.io/en/latest/) is used to handle database structure migrations. 
Whenever the data model changes, you need to manually run `flask db migrate -m "Name of migration"`
This will generate a file under `/migrations/version` which then should be checked into GIT. Whenever the API starts up, it calls `flask db upgrade`. This command will automatically apply any new migrations to the database. No manual scripts or post release commands are required!

## Extra details if the visualization script directly above was started.

6. After running step 3 OPTION B above, find the URL that appears in the terminal and go to it in your internet browser.

    Example: "Dash is running on http://127.0.0.1:8050/" appears in the terminal, so go to http://127.0.0.1:8050/ in your internet browser.


7. Use the visualization dashboard in your internet browser.

8. When done using the dashboard, close the browser and stop the script from running by going to the terminal and pressing [CTRL + C]

## Code Style
The Python code style is formatted using [Black](https://pypi.org/project/black/). Black is a file formatter that converts your code to follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards. PEP 8 provides guidelines and best practices for writing Python, and is the standard style used for modern Python libraries. 

Install Black by running `pip install black`. Note: Python 3.6.0+ is required.

Cd into the climatemind-backend directory on your computer to run black commands.

Run Black locally to see which files need formatting using `python3 -m black --check ./`

Use Black to automatically format your files using `python3 -m black ./`
