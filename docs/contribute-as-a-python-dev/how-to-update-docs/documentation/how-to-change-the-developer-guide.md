# How to change the Developer Guide

## GitBook

Gitbook is a modern documentation platform where teams can document everything from products to internal knowledge bases. As an open-source project, we are eligible to have a free license.

{% hint style="info" %}
See [GitBook documentation](https://docs.gitbook.com/getting-started/overview) for the walkthrough guide
{% endhint %}

### Invite

Using the link below you could join our GitBook organization as an editor. Editors are able to read and comment, just like a commenter, but they're also able to edit content in a couple of ways. Firstly, for spaces that are **open** for [live edits](broken-reference), editors can edit the content directly. Secondly, for spaces that have live edits **locked**, editors can create and submit [change requests](broken-reference). Editors cannot merge change requests.

{% hint style="success" %}
You can join our GitBook space using [this link](https://app.gitbook.com/invite/5XFn5ZR3pCC6X1TsNYnf/fRBlC4symWdoI5X6tBpz).&#x20;
{% endhint %}

### Summary file

The documentation created with GitBook relies on a table of the content file named [SUMMARY.md](https://github.com/ClimateMind/climatemind-backend/blob/develop/SUMMARY.md) which is not visible in GitBook UI but exists in a repository root.

### Adding new files

When you are adding new files via GitBook on a **top level** of the docs they will be located at the root of the repository. To keep the repository clean you have to do the following steps outside the GitBook:

* Move new files to the `docs` directory.
* Update `SUMMARY.md` file to reflect the correct paths to files.&#x20;

The creation of new subpages or renaming pages could also lead to this problem. See below the list of all issues to be aware of.&#x20;

### Possible issues

Managing the documentation with GitBook could be handy but sometimes lead to some annoying bugs. Due to a lack of [tests](https://github.com/ClimateMind/climatemind-backend/issues/412), you should double-check the following possible issues before merging `docs` branch into `develop`.&#x20;

* `SUMMARY.md` should contain files only from `docs` folder
* all `.md` files should be located in `docs` folder (except `README.md` and `SUMMARY.md`). Subdirectories should be also checked.&#x20;
* there are no invalid paths like `docs/docs/docs...` in the `SUMMARY.md` file
* files are not duplicated
* check that links in `.md` files are not pointing to `app.gitbook.com`
* check that links in `.md` files are pointing to existing pages.
* The first H1 title in the file should be equal to the file name. Otherwise, GitBook will create a new empty file.&#x20;

## Any other way

`.md` files could be changed like any other source code using your IDE or directly in GitHub. Since we maintain multiple documentation projects see the [documentation changing guide](https://contribute.climatemind.org/v/documentation/) to learn more.

Doing this make sure you've created a new branch from the u- to-date `docs` branch. After that create a PR to merge your changes to `docs`. The `docs` branch merged `develop` from time to time.



