# Climatemind Backend Contribution Doc

# Contents

1. Intro
2. What is this repository?
3. Dependencies and Getting Started
4. Getting in Touch and Communication
5. Change Process and how to contribute
6. Additional Resources and Information

## 1. Intro

**Hello, and welcome to the official Climatemind backend repository!**

If you've found your way here, you have likely heard of the Climatemind Project. Don't worry if you haven't! Just head on over to <a>https://climatemind.org/</a> for an intro.

This project would not exist if it wasn't for driven and curious individuals who are passionate about solving the issues of climate change.

**We thank you for being one of them.**

The information below will take you through everything you will need to know in order to contribute to the backend of Climatemind. We are firm believers in open source and as such we want to make it as easy as possible for anyone to contribute. Please do read the doc to ensure that you can get up and running as quickly as possible, and that the change request process makes sense!

## 2. What is Climatemind-Backend

Climatemind-backend contains the codebase used as part of the climatemind App. This codebase is effectively a Python API, built to serve a React frontend (if frontend dev. is more to your liking, head on over to: [https://github.com/ClimateMind/climatemind-frontend](https://github.com/ClimateMind/climatemind-frontend)).

## 3. Getting Started & Dependencies

#### Getting started with local development:

The setup requires docker. You can download it here: <a>https://www.docker.com/products/docker-desktop</a>. Once installed, run container with:

    $ docker-compose up
        
NOTE: On Windows it is running in a strict secure mode. You need to add the source directory to the Docker Resources:
    *Settings / Resources / File Sharing -> add the application root directory*.

You can also start the container in the background with:

    $ docker-compose up -d

To stop the container, run:

    $ docker-compose down

#### For deployment:

The Docker lifecycle is to build the image and run it only once. After that you can stop or start the image.

*To build:*
    
    $ docker build -t "climatemind-backend:0.1" .

*Check the built image:*

    $ docker images climatemind-backend
    
*Running Docker:*

    $ docker run -d --name climatemind-backend --publish 5000:5000 climatemind-backend:0.1

*Stopping the container:*

    $ docker stop climatemind-backend

*Starting the container:*

    $ docker start climatemind-backend

    
## 4. Main Communication Channels
The Climatemind project is run by teams, distributed all over the globe. All of the communication is done on a dedicated group of slack channels. For now, an invite is required to join a channel. Simply send off an email to: <a>hello@climatemind.org</a> to receive an invite. :)

There is a weekly “standup” usually occurring on Zoom on Sunday evenings (20:00 GMT+1) that is open for everyone that wants to join. The standup is recorded for those that cannot attend. It is recommended to join or listen to the recording in order to sync up with the other members. There is also a separate non-recorded zoom room for breakout discussions etc. 

NOTE: To get access to the rooms, please ask for an invite on Slack.

For the complete information re: what is currently worked on, what is in the project backlog etc., this is stored in our [Jira Cloud Project](https://climatemind.atlassian.net/secure/BrowseProjects.jspa). 

If you want to **suggest a new feature** it’s a good idea to discuss it in Slack with the backend team. It is also a good idea to check out the backlog in Jira to ensure that the feature isn’t already in the works. We are always looking for new ideas to collaborate on so don't be shy in suggesting new ones!
## 5. How to Contribute & Change Process

The start of your workflow should be to look at Jira and see what tasks need to be done. Jira is the tool that tracks the project's progression (effectively a kanban board). Before writing any code, head on over to [Jira Cloud Project](https://climatemind.atlassian.net/secure/BrowseProjects.jspa). Your workflow should resemble that of the below steps:

#### Workflow

1. Assign the issue to your self (or make a new story by following our story writing guide, then click 'start') then move to in progress. If there isn’t a story that accurately reflects the change you want to make, consult with the backend team on Slack.

2. To start contributing a change, first make sure you have the latest version of the project by pulling it down from github. Next, make a branch from master named in accordance with your change is trying to accomplish, for example:

        $ git checkout -b feature/{jira-issue-ID}-short-meaningful-title-of-the-branch

	Make sure you include the jira-issue-id in the branch name. This provides some nifty integration that links your branch to the Pivotal tracker :)

	Once starting the work, try to make commits onto your branch with useful and descriptive messages so that the team can understand what you are trying to accomplish and so support can be provided in the process. 

3. When you are happy with the changes you've made, proceed by going on the repository website: <a>https://github.com/ClimateMind/climatemind-backend</a> and create a **pull request** for your changes to be merged into master.

	If the climatemind repo has changed significantly between the time you started and finished your changes, you may be asked to rebase your branch. You can read more about what this means here: <a>https://git-scm.com/book/en/v2/Git-Branching-Rebasing</a>s

4. After at least one approval by a maintainer, the branch will be merged and you must the branch. The project follows the PEP8 style standard and any change that does not comply with PEP8 will be forced to do so before being merged.

5. Once your change is integrated, make sure you change the Pivotal story status to capture the conclusion of the change.

If you have any questions or thoughts, please don't hesitate to reach out on Slack :)
## 6. Additional Resources and Information

Here’s a quick collection of resources if you need to readup on the various libraries and technologies used:

Flask (webdev framework): <a>https://flask.palletsprojects.com/en/1.1.x/quickstart/</a>


NetworkX (graph analytics): <a>https://networkx.github.io/</a>

Owl2ready (Python Ontology wrapper): <a>https://pypi.org/project/Owlready2/</a>

Docker (containerization framework): <a>https://www.docker.com/get-started</a>
