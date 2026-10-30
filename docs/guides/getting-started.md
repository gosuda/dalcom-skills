# Getting started

Install the base plugins, confirm the install, and run one skill. That is the whole tutorial.

## Install the plugins

Add the `dstack` marketplace from repository `gosuda/dalcom-skills`, then install `dstack-core` followed by `dstack-code`. These two form the base engineering set:

```shell
claude plugin marketplace add gosuda/dalcom-skills
claude plugin install dstack-core@dstack
claude plugin install dstack-code@dstack
```

In Codex, register the marketplace and add the plugins:

```shell
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-core@dstack
codex plugin add dstack-code@dstack
```

For specialized workflows, install the companion plugins `dstack-planning`, `dstack-run`, and `dstack-knowledge`:

```shell
claude plugin install dstack-planning@dstack
claude plugin install dstack-run@dstack
claude plugin install dstack-knowledge@dstack
```

## Confirm the install

List your installed plugins. On Claude Code the command is `claude plugin list`, and [`install-proof`](../specs/install-proof.md) records the run that proves it: the list shows each plugin with its version, scope, and status. If the installed plugins appear as enabled, your client resolved this tree.

## Run one skill

Type a skill invocation with a request after it:

```text
/dstack-core:necessary-work Is this change really needed, or is the task already done?
```

That is the Claude Code spelling; in Codex type `$necessary-work` and the same request.

`necessary-work` asks whether the work stays inside the ask, so it fits a first run: you read the answer and judge it at once.

What happened: the skill's instructions were prepended to your request, and the model answered both together. That is all an invocation does.

## Next steps

[Using skills](using-skills.md) covers the mechanics: stacking invocations, passing files, and choosing between overlapping skills. [Workflows](workflows.md) shows chains of skills that real sessions proved out.
