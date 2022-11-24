# Unit tests

{% hint style="info" %}
Python unit tests are the primary step in our [Continuous Integration ](ci-continuous-integration.md)pipeline.
{% endhint %}

Unit testing in a nutshell is just providing some inputs to the function (unit) and checking if the result is the same as expected. You need to think out all possible kinds of inputs that could lead to error output. Unit tests reduce defects in the newly developed features or reduce bugs when changing the existing functionality.

## PyTest

We are using [PyTest](https://docs.pytest.org/en/6.2.x/getting-started.html) a framework that makes building simple and scalable tests easy. Tests are expressive and readable - no boilerplate code is required.

To run `pytest` unit tests you need to [execute](work-with-docker.md#execute-command-in-docker-container) the `pytest` command in the docker container. See below the list of useful arguments you could use with it:

* `-x` exit instantly on the first error or failed test
* `--pdb` start the interactive Python debugger on errors or `KeyboardInterrupt`
* `-s` shortcut for `--capture=no` to show all logging
* `--cov-report html --cov` to see the HTML code coverage report on your local
* `-m MARKEXPR` only run tests matching the given mark expression. For example: `-m 'mark and not mark2'`.
* positional argument: `file_or_dir`

## How to get started writing unit tests

The best way to learn how to write unit tests is to search in the repo for similar test cases.

Each python module in our flask app should contain a `test` subfolder which contains files with names like `test_MODULE_FILE.py`

## Code coverage

TODO
