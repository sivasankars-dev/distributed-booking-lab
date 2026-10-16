# Learning notes

**Test your own device.** Results vary by hardware, configuration, workload, and background activity. Published results are examples, not scores to match. Observations and possible explanations belong in separate sections. CPU percentages do not directly measure remaining request capacity.

## Published notes

| Learner | Task | Record |
| --- | --- | --- |
| Siva | Task 01 baseline | [Four historical runs recorded on 2026-10-16](siva/task-01-baseline.md) |

The historical note preserves its measurements and missing environment details. It is not a new runtime verification of these task instructions.

## Add your own note

Copy the [Task 1 template](../../labs/task-01-baseline/results-template.md) or [Task 2 template](../../labs/task-02-pool-waiting/results-template.md) into `docs/learning-notes/<your-name>/task-NN-topic.md`. Use a distinct filename for additional experiments or clearly dated runs within your own report. Task 2 requires implementation before collecting results.

Record commit and uncommitted changes, effective configuration, commands, correctness evidence, raw-output references where available, limitations, and reset steps. Write `Not recorded` rather than guessing missing values, and `Not applicable` only when a measurement does not apply. Preserve failed and interrupted runs too.

Do not edit Siva's historical measurements to match your machine. Link to reports rather than duplicating them. Follow the [learner Git workflow](../contributing-tasks.md).
