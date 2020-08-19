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

