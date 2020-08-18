# Climatemind Backend

## Running the application with Docker

Building Docker image

    docker build -t "climatemind-backend:0.1" .
    
Checking the built image

    docker images climatemind-backend
    
Running Docker

    docker run --name climatemind-backend --publish 5000:5000 climatemind-backend:0.1



