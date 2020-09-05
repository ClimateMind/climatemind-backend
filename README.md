# Climatemind Backend

Using Docker you need to install it first: https://www.docker.com/products/docker-desktop

On Windows it is running in a strict secure mode. You need to add the source directory to the Docker Resources: Settings / Resources / File Sharing -> add the application root directory

## Running the application with Docker Compose (for development)

Start in foreground (good for debugging flask and see the logs). You can stop it with [CMD + C] on OSX or [CTRL + C] on Windows or Linux.
 
    docker-compose up
    
Start in background

    docker-compose up -d
    
Stop the container which is running in the background

    docker-compose down

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


## Processing any new Climate Mind OWL ontology file

Follow these instructions to process a new version of a Climate Mind ontology OWL file into files used by Climate Mind (such as Networkx pickle file, test ontology JSON, edge list output CSV, etc). 

1. Download the new OWL ontology file (if haven't already) and make note of the absolute path. DO NOT SAVE the OWL file in the Climate Mind directory in order to avoid accidentally pushing it to the repo.

2. From the climatemind-backend directory run the process_new_ontology_file.py with the absolute path to the new OWL file from step 1. 
    
    Example: python3 process_new_ontology_file.py ABSOLUTE_PATH_TO_OWL_FILE

3. New files will be generated and appear in the climatemind-backend directory. These files are also listed in the git.ignore file, so don't worry about them getting pushed accidentally to the git repo.


## Visualizing the ontology

Follow these instructions to visualize an OWL file using the Dash dashboard generated by the visualize.py script.

1. Download the new OWL ontology file (if haven't already) and make note of the absolute path. DO NOT SAVE the OWL file in the Climate Mind directory in order to avoid accidentally pushing it to the repo.

2. From the climatemind-backend directory run the process_new_ontology_and_visualize.py with the absolute path to the new OWL file from step 1. 
    
    Example: python3 process_new_ontology_and_visualize.py ABSOLUTE_PATH_TO_OWL_FILE

3. Find the URL that appears in the terminal and go to it in your internet browser.

    Example: "Dash is running on http://127.0.0.1:8050/" appears in the terminal, so go to http://127.0.0.1:8050/ in your internet browser.

4. Use the visualization dashboard in your internet browser.

5. When done using the dashboard close the browser and stop the script from running by going to the terminal and pressing [CMD + C] on OSX or [CTRL + C] on Windows or Linux.


