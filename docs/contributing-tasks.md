# Contributing tasks and Git workflows

## Shared learning structure

Published tasks live together on maintained `main` under `labs/task-NN-topic/`. `main` means the working baseline plus available task documents and implemented features, not everyone's personal experimental changes. Readiness labels distinguish available code from implementation exercises. Permanent topic branches are not the only way to access lessons.

Each task directory contains `README.md`, `concept.md`, `questions.md`, and `results-template.md`. Personal observations belong under `docs/learning-notes/<name>/`. Keep the existing baseline script in `loadtests/baseline.js`; future task scripts should be separate only when they implement real behaviour.

## Inspect before changing branches

Run these from the repository root:

```bash
git status --short
git branch --show-current
git diff
git diff --cached
```

Review untracked files too. Do not switch to `main`, reset, or clean blindly when work is present. Preserve it on its current branch with a deliberate commit or another understood backup before changing bases. Uncommitted changes can follow you across branches; a branch name alone does not isolate them.

## Maintainer workflow

`main → feat/task-NN-topic → validate → review → merge into main`

Once your tree is clean and your local `main` is the intended maintained base, an example for a future contribution is:

```bash
git switch main
git switch -c feat/task-02-pool-waiting
```

Implement only the agreed scope, validate it, review the diff, and submit for review. Merge the reviewed contribution into `main` through the repository's review process. A documentation-only contribution must not claim an endpoint exists merely because its exercise is written. Do not include personal experiment results as unexplained baseline code changes.

## Learner workflow

`own fork/local main → practice/task-NN-name → experiment → commit/push to own branch`

After preserving existing work and confirming your base:

```bash
git switch main
git switch -c practice/task-01-baseline
```

Experiment, record evidence, and inspect the diff. Stage only intended files, commit your work, and optionally push your practice branch to your own fork. Before pushing, use `git remote -v` to confirm `origin` is yours. For the example branch, the optional command is:

```bash
git push -u origin practice/task-01-baseline
```

Pushing a branch publishes that branch; it does not merge it into `main`. Avoid committing `.env` or secret-bearing output. Do not overwrite another learner's notes.

### A harder experiment from completed easy work

Commit the completed easy experiment first and confirm a clean working tree. Then branch from it:

```bash
git switch practice/task-01-baseline
git switch -c practice/task-01-harder-traffic
```

The harder branch inherits the easy branch's commits. Record that base and what you change next.

### A fresh experiment from main

After preserving any current work, return to your maintained baseline and branch anew:

```bash
git switch main
git switch -c practice/task-02-pool-waiting
```

This excludes personal changes found only on the earlier practice branch. Do not assume a branch switch resets database volumes or local environment settings; reset experiment state separately.

## Required task content

Each task README must state the production scenario, outcomes, prerequisites, readiness, concept link, starting state, permitted files, preserved interfaces, prediction, steps, available commands, measurements/correctness checks, completion criteria, reset, questions link, and results-template link.

Concept documents explain terms before using them, include an everyday analogy and API/database example, and distinguish established facts, assumptions, and predictions. Questions group Easy, Medium, and Hard reasoning and implementation challenges with no answers, worked solutions, answer keys, or solution links. Label future components and advanced knowledge; do not assume absent telemetry exists.

Describe feature enablement, validation, pool/resource limits, timeouts, cleanup, and baseline compatibility before calling an implementation ready. Runtime isolation must acknowledge shared PostgreSQL and host resources. Publish actual commands only when their required code exists; label proposed names and settings explicitly.

## Review and validation

Check local Markdown links/anchors, compare commands and behaviour with code, inspect the full Git diff, and run `git diff --check`. Include untracked documents in the review. For runtime changes, perform relevant correctness and compatibility tests and record what was actually run. A documentation inspection is not runtime verification.

Preserve historical measurements and missing-value labels. Move a historical report once, keep an index at its old path, and avoid copying the entire report into multiple places. State hardware, configuration, workload, and background activity; examples are not scores to match. Keep observations separate from explanations, and do not infer remaining request capacity directly from CPU percentages.
