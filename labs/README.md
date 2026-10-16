# Learning tasks

Start with [Start Here](../docs/start-here.md), then complete Task 1 before implementing Task 2.

| Task | Focus | Status |
| --- | --- | --- |
| [01 — Baseline](task-01-baseline/README.md) | Traffic, latency, correctness, and resource measurements | Ready to try |
| [02 — Pool waiting](task-02-pool-waiting/README.md) | Connection holding time, acquisition waiting, and timeouts | Planned — requires application implementation before running |

## Readiness labels

- **Planned:** required runtime components are unavailable. Read, predict, and implement on your own practice branch before running the exercise.
- **Ready to try:** instructions and required functionality are available and have been checked against the code. This does not mean the instructions were run during this documentation change.
- **Verified:** an experiment was executed in a documented environment with commands, configuration, results, and correctness evidence. Verification applies to that environment and revision, not every computer.

[Siva's baseline history](../docs/learning-notes/siva/task-01-baseline.md) records earlier runs with some missing environment details. It does not verify every step of the newly published task.

## How to use a task

Read its README and concept guide, write a prediction, perform the implementation or experiment, check correctness, and use its results template. Questions are grouped into Easy, Medium, and Hard without answers or solution links. Challenges identify future components or advanced knowledge where needed.

All published lessons coexist on maintained `main` in isolated directories. You do not need permanent topic branches to access lessons. Follow the [Git workflows](../docs/contributing-tasks.md) for personal experiments. Run experiments sequentially unless a task explicitly studies interference: separate modules and pools still share PostgreSQL and host resources.
