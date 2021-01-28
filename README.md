# Climatemind Backend

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project uses Docker. Install it through their website: https://www.docker.com/products/docker-desktop

**_Before doing what's below, be sure the Docker application is running and the command line working directory is changed to the climatemind-backend path._**

## Running the application with Docker Compose (for development)

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

## Running the application with Docker (for deployment)

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

[Swagger Documentation](http://localhost:5000/swagger) is available, detailing the API endpoints and how they should be used. Whilst in development this can be found at [http://localhost:5000/swagger](http://localhost:5000/swagger).

---

## Processing a new Climate Mind OWL ontology file

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

