# CI - Continuous Integration

Manual testing by developers is time-consuming and unreliable. The lack of a QA team does not allow for testing the whole project on each change. Insufficient software testing increases the chance of developer complications and bad user experiences.

CI solves the problem of insufficient testing by laying the foundation of automated test suites. By monitoring the central code repository and running tests on every change, CI collects test results and communicates them to the entire team working on the project.

## CircleCI

We are using the continuous integration and [continuous delivery](cd-continuous-delivery.md) platform [CircleCI](https://circleci.com/). Our project pipelines are located [here](https://app.circleci.com/pipelines/github/ClimateMind/climatemind-backend). After each push to the origin, you will be able to see a pipeline running for your branch.

CI setup is stored in the `.circleci/config.yml` file and consists of the following jobs:

* `lint` - checking that the [coding style](code-style.md) is adhered to
* `pytest` - checking the [unit tests](unit-tests.md)

{% hint style="warning" %}
Note: If any test jobs fail, the [PR](making-a-pr.md) with changes is not permitted to merge to the develop branch.
{% endhint %}
