# Climatemind Backend

[![CircleCI](https://circleci.com/gh/ClimateMind/climatemind-backend/tree/develop.svg?style=shield)](https://app.circleci.com/pipelines/github/ClimateMind/climatemind-backend?branch=develop) [![codecov](https://codecov.io/gh/ClimateMind/climatemind-backend/branch/develop/graph/badge.svg?token=6OBPBQ6OBP)](https://codecov.io/gh/ClimateMind/climatemind-backend) ![GitHub](https://img.shields.io/github/license/ClimateMind/climatemind-backend)

## Table of Contents

1. [What is this repo?](./#what-is-this-repo)
2. [How this works](./#how-this-works)
3. [Overview](./#overview)
4. [Installing the Project](./#installing-the-project)
5. [Installing Docker](./#installing-docker)
6. [Installing the Ontology-Processing Repo](./#install-the-ontology-processing-repo)
7. [Process the Ontology](./#process-the-ontology)
8. [Running the application](./#running-the-application)
9. [Local API](./#local-api)
10. [Local App](./#local-app)
11. [Backend Debugging](./#backend-debugging)
12. [API Documentation](./#api-documentation)
13. [FAQ](./#faq)

## What is this repo?

The [Climate Mind application](https://app.climatemind.org) makes conversations about climate change easier, by letting users explore climate issues that speak to their personal values. We aim to inspire users to take action with a range of attractive solutions consistent with their values that they can get excited about.

The application currently presents solutions based on the user's personal values (as determined by a questionnaire) and their location (zip code). In the future, we plan to add the user's occupation as an option to personalize the results.

## How this Works

In order to serve users with relevant climate information our data team has organized climate data into an Ontology. Don't let the fancy term overwhelm you, as it is (at the end of the day) just a data structure. It contains information about the relationships between climate issues, solutions, myths, and other data.

However, this data structure, in its native form, is not easy to work with. We have another repo [climatemind-ontology-processing](https://github.com/ClimateMind/climatemind-ontology-processing) which does all of the hard work to convert this data into an easy to work with graph structure (known as NetworkX). This graph is packaged into the .gpickle file found in the /output directory and read by the application.

Detailed instructions for processing the ontology can be found [below](./#owl-file-processing) or in the [climatemind-ontology-processing repo](https://github.com/ClimateMind/climatemind-ontology-processing).

## Overview

In order to use this application you need to:

1. Install the project
2. Install Docker
3. Install the Ontology Processing repo through Pip
4. Download the Ontology file and process it to create the .gpickle
5. Build the application with Docker
6. Launch the application with Docker

Following are more details about each of these steps

## Installing the Project

To intall the code to your local machine, navigate to the desired parent folder via the command line and clone the repo

```
git clone https://github.com/ClimateMind/climatemind-backend.git
```

You will now have access to our backend code.

## Installing Docker

Install [Docker](https://www.docker.com/products/docker-desktop) through their website.

## Process the Ontology

_**Follow these steps every time you are made aware of an update to the Ontology.**_

1. Download a fresh copy of the ontology from web protege. Make sure it's the RDF/XML format (check the downloaded item has .owl at the end of it!).
2. Run the `process_owl` flask command by executing the following (replace `<relative/path/filename.owl>`):

```
flask ontology process_owl <relative/path/filename.owl>
```

Use `--no-check` argument to skip comparison with the previous ontology.

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

## Local API

If you'd like to test the endpoints, you can do this with Postman.

Register for and install Postman from their [website](https://www.postman.com).

We have a collection of tests already available that you can run. Request access from any of the backend team members to our collections.

## Local App

If you'd like to test the application locally with the front-end interface, you need to do the following:

### First Time

1. Use terminal/command-line to navigate to any directory located outside of the climatemind-backend
2. Clone the front-end repo

```
git clone https://github.com/ClimateMind/climatemind-frontend.git
```

1. Install NPM

```
npm -i
```

### Every Time

1. Navigate to the /climatemind-backend directory
2. Start the Docker Instance and attach to it

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up -d
docker attach climate-backend_web_1
```

1. Open up a second terminal/command-line instance
2. Navigate to the /climatemind-frontend directory
3. Start NPM

```
npm start
```

You should now be able to open [http://localhost:3000/](http://localhost:3000/) or [http://127.0.0.1:3000/](http://127.0.0.1:3000/) and have access to the fully functioning application locally!

***

## Backend Debugging

The app can be debugged using pdb. You can do this several ways.

1. Use Postman to test the API without a front-end instance
2. Use the front-end instance to interact with the API
3. Run specific `pytest` unit test inside the backend container `docker exec -it climatemind-backend_web_1 pytest -xs --pdb YOURTEST`

For either test, you need to add a breakpoint() into the code where you want the application to pause for debugging.

For more information about PDB review their [documentation](https://docs.python.org/3/library/pdb.html).

**To test with Postman**

Navigate to the climatemind-backend directory and run:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up -d
docker attach climatemind-backend
```

The terminal/command-line can now be used to interact with PDB. Once the code hits a stopping point, you will see (pdb) in this terminal/command-line instance.

**To test with Front-End**

Run the same commands listed above. Then open up a second terminal and run:

```
npm start
```

The terminal/command-line can now be used to interact with PDB. Once the code hits a stopping point, you will see (pdb) in this terminal/command-line instance.

## API documentation

[AutoDoc](http://localhost:5000/documentation) Our API is currently documented using AutoDoc. This will soon be deprecated and replaced with Swagger.

[Swagger Documentation](http://localhost:5000/swagger) will be available soon, detailing the API endpoints and how they should be used. Whilst in development this can be found at [http://localhost:5000/swagger](http://localhost:5000/swagger).

***

## FAQ

**Q: Is Docker needed to process the ontology?** A: No, Docker has nothing to do with the ontology processing

**Q: Which files need to be in the repo for the app to have access to the data?** A: The .gpickle file needs to be in the climatemind-backend/output folder. As long as it has this file, the app will have data to work with. _The OWL File is not needed in the backend-repo_

**Q: How does the production application get access to the climate data?** A: The .gpickle file is included in the commits to the repo. When this is pushed to the main branch, the production application has access to the .gpickle file

**Q: Where can I find more information about contributing to the project?** A: You will find a guide to contributing and other documentation relevant to the project in the [docs](https://github.com/ClimateMind/climatemind-backend/tree/develop/docs) folder.

## Special Thanks

Git history loses contributions when a file is moved, so thank you to the following people who worked on the previous version. @NickCallaghan @biotom @rodriguesk @znurgl @y-himanen
