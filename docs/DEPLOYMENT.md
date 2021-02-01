# Deployment

Deployment should be performed by an experienced team member with access to Azure.

TODO @rodriguesk should update these instructions.

## Running the application with Docker (for deployment)

**_If you are a new developer on the team, you do not need to do this._**

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
