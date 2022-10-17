# How to merge docs changes

When changes are in `docs` branch they could be merged to `develop` branch. &#x20;

1. Create a Push Request from `develop` <- `docs`.
2.  Update with rebase `docs` branch using UI in PR.&#x20;

    <figure><img src="../../../.gitbook/assets/Screenshot 2022-10-13 at 13.34.00.png" alt=""><figcaption><p>Update the docs branch</p></figcaption></figure>
3.  Create a simple merge commit, **without** squash or rebase.

    <figure><img src="../../../.gitbook/assets/Screenshot 2022-10-13 at 13.09.53.png" alt=""><figcaption><p>Merge docs to develop using simple merge</p></figcaption></figure>

The final git tree will look like this. GitBook should be able to handle it without any issues.&#x20;

<figure><img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVb0Qqfe4f2Rsrb5b45qY%2Fuploads%2Fk10cj9gut5CfS5hX9xDe%2FScreenshot%202022-10-13%20at%2013.36.41.png?alt=media&#x26;token=c241ae80-dea8-44bd-9efe-931419dd6e54" alt=""><figcaption></figcaption></figure>
