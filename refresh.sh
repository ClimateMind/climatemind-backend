#!/bin/bash

# I need to refresh every time I change code or docker won't import it into the web service


# take down current running backend environment
docker-compose down 

# clean up any dangling images
docker system prune -y

# bring back up (and rebuild?)
docker-compose up -d

# save web container id after instantiation
WEB=$(docker ps -lq)

DO="docker exec -it $WEB python -m"

# temp dependencies I didn't want to add into requirements.txt
# and, run debugger on script that calls make_graph.py
$DO pip install ipdb ipython && \
$DO ipdb process_new_ontology_file.py

