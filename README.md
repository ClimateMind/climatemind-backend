# Climatemind Backend

## Running the application with Docker Compose

    docker-compose up

## Running the application with Docker

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

