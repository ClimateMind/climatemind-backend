# Making a PR

Create a pull request to propose and collaborate on changes to a repository. These changes are proposed in a branch, which ensures that the default branch only contains finished and approved work.

## Before making a PR

1. Test your code locally using [Postman](debugging.md) to ensure that the endpoints return valid responses.
2. Format your code using [PEP8 Styling](code-style.md)
3. If your changes affect how the app is run, please [modify the documentation](../how-to-update-docs/) accordingly.
4. If your functionality needs to be tested, please include at least one[ unit test](unit-tests.md).

{% hint style="info" %}
See the [GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) to find out how to create your first Pull Request to merge changes to `develop` <- from `your branch`
{% endhint %}

## Before requesting a review

1. Update your feature branch with rebase from develop branch to apply your changes on top of the most recent commit from develop. It's possible to do this using GitHub UI directly on the Pull Request page
2. Squash your commits into single one or logical steps if needed (e.g. 1. implementing a feature, 2. refactoring). Make sure there are no small commits like `linting` or `cosmetics`.
3. Ensure that the lint and [CI checks](ci-continuous-integration.md) pass.

{% hint style="info" %}
See [GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review) to see how to request a review.
{% endhint %}

## After PR review

The reviewer should merge the feature branch after giving an approval review.
