# Under the hood

## Our stack

* Python v3.8.5
* Flask v1.1.2
* MSSQL
* Azure

## How this Works

In order to serve users with relevant climate information, our data team has organized climate data into an Ontology. Don't let the fancy term overwhelm you, as it is (at the end of the day) just a data structure. It contains information about the relationships between climate issues, solutions, myths, and other data.

However, this data structure, in its native form, is not easy to work with. We have another repo [climatemind-ontology-processing](https://github.com/ClimateMind/climatemind-ontology-processing) which does all of the hard work to convert this data into an easy to work with graph structure (known as NetworkX). This graph is packaged into the .gpickle file found in the /output directory and read by the application.

Detailed instructions for processing the ontology can be found [below](under-the-hood.md#owl-file-processing) or in the [climatemind-ontology-processing repo](https://github.com/ClimateMind/climatemind-ontology-processing).

## Additional Resources

1. [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
2. [NetworkX](https://networkx.github.io/)
3. [Owl2Ready](https://pypi.org/project/Owlready2/)
4. [Docker](https://www.docker.com/get-started)
