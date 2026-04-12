---
layout: single
title: GitHub Actions for pull requests
date: 2021-05-30
categories: github ci
---

GitHub Actions provides a well-integrated CI/CD system for code hosted on
GitHub.  If you want to build and run tests when someone sends pull requests,
you can use the [pull_request event][pull-request-event].  The `pull_request`
event runs the workflow in a security-hardened environment due to [security
reasons][security-reasons].  For example, the [encrypted
secrets][encrypted-secrets] deposited in GitHub will not be available for the
workflow.  Another restriction is that the `GITHUB_TOKEN` [only gets read
access][permissions-for-the-github_token] with the pull_request event type.

If you want some write operations after the build and tests, you can use the
[workflow run event][workflow-run-event].  It requires some preparation from the
`pull_request` job.  You can save the pull request number, build outputs, test
results, and all other workflow data into one directory, say `pr`, and [store it
as an artifact][artifact].

Here is an example to upload the `pr` directory as an artifact.  It will be
available as `pr.zip` in the workflow run for 90 days (by default):

```yaml
      - uses: actions/upload-artifact@v2
        with:
          name: pr
          path: pr/
```

From the [workflow run event][workflow-run-event], you can download the stored
artifact.  You can see an example in the [Keeping your GitHub Actions and
workflows secure][security-reasons] article.  Since the workflow run got write
access, you can perform write operations based on the downloaded artifacts.
Some of the common write operations are adding comments and labels to the pull
requests.

Yet another restriction with the pull request event is [manual
approval][manual-approval] required for the first-time contributors' pull
request.  The requirement for manual approval is an ongoing [issue with some
workarounds][manual-approval-workarounds].

[pull-request-event]: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#pull_request
[security-reasons]: https://securitylab.github.com/research/github-actions-preventing-pwn-requests/
[encrypted-secrets]: https://docs.github.com/en/actions/reference/encrypted-secrets
[permissions-for-the-github_token]: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
[workflow-run-event]: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#workflow_run
[artifact]: https://docs.github.com/en/actions/guides/storing-workflow-data-as-artifacts
[manual-approval]: https://github.blog/2021-04-22-github-actions-update-helping-maintainers-combat-bad-actors/
[manual-approval-workarounds]: https://github.community/t/how-to-auto-approve-workflow-runs-for-first-time-contributors/176436
