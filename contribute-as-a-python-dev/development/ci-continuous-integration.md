# CI - Continuous Integration

Manual testing by developers is time-consuming and not reliable. The lack of a QA team does not allow to test the whole project on each change. Insufficient software testing increases the chance of developer complications and bad user experiences.

CI solves the problem of insufficient testing by laying the foundation of automated test suites. By monitoring the central code repository and running tests on every change that is made, CI collects test results and communicates them to the entire team working on the project.

## CircleCI

We are using the continuous integration and [continuous delivery](cd-continuous-delivery.md) platform [CircleCI](https://circleci.com/). Our project pipelines are located [here](https://app.circleci.com/pipelines/github/ClimateMind/climatemind-backend). After each push to the origin, you will be able to see a pipeline running for your branch.&#x20;

CI setup stored in the `.circleci/config.yml` file and consist of the following jobs:

* `lint` - checking that the [coding style](../../docs/contribute-as-a-python-dev/development/code-style.md) is performed
* `pytest` - checking the [unit tests](../../docs/contribute-as-a-python-dev/development/unit-tests.md)

{% hint style="warning" %}
Note that if one of the jobs will fail [PR](making-a-pr.md) with changes is not permitted to merge to the develop branch.
{% endhint %}



