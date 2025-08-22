# Contributing Guide

Thank you for investing your time in contributing to Eclipse BaSyx and the BaSys middleware.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR on GitHub.

Furthermore, it gives some guidelines on how to write your own entry in the documentation.

## Contribute Changes

Here's the standard workflow to contribute changes to Eclipse BaSyx Projects (including the wiki).

Before contributing, please make sure, you fill out the [Eclipse Contributor Agreement (ECA)](https://www.eclipse.org/legal/ECA.php). This is done by creating an Eclipse account for your git e-mail address and then submitting the following form: [https://accounts.eclipse.org/user/eca](https://accounts.eclipse.org/user/eca). The e-mail address used to sign the ECA is the same one that needs to be used for committing.

After this, the workflow to submit contributions to Eclipse BaSyx is pretty standard, as the picture below shows:

```{figure} ./images/workflow-contributing.png
---
width: 100%
alt: Contributing to Eclipse BaSyx
name: contributing
---
```

1. Fork the respective Eclipse BaSyx Repository
2. Clone your fork to your development machine and add Eclipse-BaSyx as `upstream`:

```bash
# Example for the Wiki
git clone https://github.com/<your-github-username>/basyx-wiki
cd basyx-wiki
git remote add upstream https://github.com/eclipse-basyx/basyx-wiki
```

1. Pull the branch you want to contribute to (e.g. main):

```bash
git checkout -b <your-branch-name> upstream/<branch-name>
```

Now, you can create a new local branch in which you can create your changes and actually do your changes. When you're done with that, continue with:

4. Push the new branch to your fork:

```bash
git push origin <your-branch-name>
```

5. Create a Pull Request from your fork `<your_new_branch>` to the Eclipse BaSyx Repository `<branch_name>`

The Eclipse BaSyx maintainers will then review the pull request and communicate the further steps via the comments.
