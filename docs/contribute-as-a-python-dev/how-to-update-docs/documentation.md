# Backen documentation

## Overview

### Format

markdown

### GitBook



## How to make changes

### Change in GitBook

invoice, possible issues&#x20;

### Any other way

make PR to docs first



## How to merge docs branch to develop

When changes are in `docs` branch they could be merged to `develop` branch. &#x20;

1. Create a Push Request from `develop` <- `docs`.
2.  Update with rebase `docs` branch using UI in PR.&#x20;

    <figure><img src="../../.gitbook/assets/Screenshot 2022-10-13 at 13.34.00.png" alt=""><figcaption><p>Update the docs branch</p></figcaption></figure>
3.  Create a simple merge commit, **without** squash or rebase.

    <figure><img src="../../.gitbook/assets/Screenshot 2022-10-13 at 13.09.53.png" alt=""><figcaption><p>Merge docs to develop using simple merge</p></figcaption></figure>

The final git tree will look like this. GitBook should be able to handle it without any issues.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2022-10-13 at 13.36.41.png" alt=""><figcaption></figcaption></figure>
