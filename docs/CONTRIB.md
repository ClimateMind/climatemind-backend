# Contributing to Climate Mind

## Contents

1. Intro
2. Communication Channels
3. Making a PR
4. Reviewing a PR
5. Merging
6. Code Style
7. Additional Resources


**Hello, and welcome to the official Climatemind backend repository!**

If you've found your way here, you have likely heard of the Climatemind Project. Don't worry if you haven't! Just head on over to <a>https://climatemind.org/</a> for an intro.

This project would not exist if it wasn't for driven and curious individuals who are passionate about solving the issues of climate change.

**We thank you for being one of them.**

At the moment, we do not accept anonymous PRs, but we'd love to recruit some more volunteers to be consistent 
members of our team. If you are interested in joining us, please [reach out to us.](https://climatemind.us18.list-manage.com/subscribe?u=a8795c1814f6dfd3ce4561a17&id=b451cfd1ed)

Or email us at [hello@climatemind.org](hello@climatemind.org) with your Resume and Github.

## Communication Channels

The Climatemind project is run by teams, distributed all over the globe. All of the communication is done on a dedicated group of slack channels. For now, an invite is required to join a channel. Simply send off an email to: hello@climatemind.org to receive an invite. :)

There is a weekly “standup” usually occurring on Zoom on Sunday evenings (20:00 GMT+1) that is open for everyone that wants to join. The standup is recorded for those that cannot attend. It is recommended to join or listen to the recording in order to sync up with the other members. There is also a separate non-recorded zoom room for breakout discussions etc.

NOTE: To get access to the rooms, please ask for an invite on Slack.

## How to Contribute

Our project management is handled in Jira. If you don't already have access to our Jira, please request access from someone on the team.

If you're assigned a task in Jira, make sure to use the ticket number in your branch name. For example, if the ticket is CM-57 you could make `CM-57-Fixing-API-Errors` as a name.

If you want to suggest a new feature it’s a good idea to discuss it in Slack with the backend team. It is also a good idea to check out the backlog in Jira to ensure that the feature isn’t already in the works. We are always looking for new ideas to collaborate on so don't be shy in suggesting new ones!

## Making a PR

We have limited credits with CircleCI. It's fine to make commits or PRs as needed, but before making a PR please do the following:

1. Test your code locally using Postman to ensure that the endpoints return valid responses.
2. Format your code using Pep8 Styling (see below)
3. If your changes affect how the app is run, please modify the documentation accordingly.
4. If your functionality needs to be tested, please include at least one test.
4. Ensure that the lint and build tests pass before requesting a review.

## Reviewing a PR

1. If the code is modified, make sure to pull the branch and test that the endpoints are working.
2. Make sure the code has passed linting and black before approving

## Merging

The original contributor should merge their branch after receiving one approval review.

## Code Style

The Python code style is formatted using [Black](https://pypi.org/project/black/). 
Black is a file formatter that converts your code to follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards. 
PEP 8 provides guidelines and best practices for writing Python, and is the standard style used for modern Python libraries. 

Open the terminal/command line and install Black by running `pip install black`. Note: Python 3.6.0+ is required.

1. Use the terminal/command-line to navigate to the climatemind-backend directory
2. Run Black locally to see which files need formatting using `python3 -m black --check ./`
3. Use Black to automatically format your files using `python3 -m black ./`

## Additional Resources

1. [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
2. [NetworkX](https://networkx.github.io/)
3. [Owl2Ready](https://pypi.org/project/Owlready2/)
4. [Docker](https://www.docker.com/get-started)


