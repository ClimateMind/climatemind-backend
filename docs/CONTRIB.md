# Contributing to Climate Mind

Thank you for your interest in contributing to Climate Mind. At the moment, we do not accept anonymous PRs, 
but we'd love to recruit some more volunteers to be consistent members of our team. If you are interested in joining us,
please [reach out to us.](https://climatemind.us18.list-manage.com/subscribe?u=a8795c1814f6dfd3ce4561a17&id=b451cfd1ed)

Or email us at [hello@climatemind.org](hello@climatemind.org) with your Resume and Github.

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


