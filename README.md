# Climatemind Backend

[![CircleCI](https://circleci.com/gh/ClimateMind/climatemind-backend/tree/develop.svg?style=shield)](https://app.circleci.com/pipelines/github/ClimateMind/climatemind-backend?branch=develop) [![codecov](https://codecov.io/gh/ClimateMind/climatemind-backend/branch/develop/graph/badge.svg?token=6OBPBQ6OBP)](https://codecov.io/gh/ClimateMind/climatemind-backend) ![GitHub](https://img.shields.io/github/license/ClimateMind/climatemind-backend)

## Table of Contents

1. [What is this repo?](./#what-is-this-repo)
2. [How this works](./#how-this-works)
3. [Overview](./#overview)

## What is this repo?

The [Climate Mind application](https://app.climatemind.org) makes conversations about climate change easier, by letting users explore climate issues that speak to their personal values. We aim to inspire users to take action with a range of attractive solutions consistent with their values that they can get excited about.

The application currently presents solutions based on the user's personal values (as determined by a questionnaire) and their location (zip code). In the future, we plan to add the user's occupation as an option to personalize the results.

## How this Works

In order to serve users with relevant climate information, our data team has organized climate data into an Ontology. Don't let the fancy term overwhelm you, as it is (at the end of the day) just a data structure. It contains information about the relationships between climate issues, solutions, myths, and other data.

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

## Special Thanks

Git history loses contributions when a file is moved, so thank you to the following people who worked on the previous version. @NickCallaghan @biotom @rodriguesk @znurgl @y-himanen
