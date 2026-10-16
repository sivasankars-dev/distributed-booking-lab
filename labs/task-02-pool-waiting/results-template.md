# Task 02 results template

**Planned — requires application implementation before running.** Record predictions now; fill measured results only after implementing and running the task.


Copy this template into your own file under `docs/learning-notes/<name>/`. Replace prompts with evidence; use `Not recorded` for missing values. Estimates and predictions are not measurements. Results vary by hardware, configuration, workload, and background activity. Published results are examples, not scores to match.

## Goal and prediction

- Production question:
- Prediction before running:
- Assumptions:
- Evidence that would contradict the prediction:

## Environment and revision

| Field | Recorded value |
| --- | --- |
| Learner | Not recorded |
| Date, time, timezone | Not recorded |
| Git branch and full commit | Not recorded |
| Uncommitted tracked and untracked changes | Not recorded |
| Computer model, CPU, core count, RAM | Not recorded |
| OS and version | Not recorded |
| Docker Engine/Desktop and Compose versions | Not recorded |
| Docker CPU/memory limits and any container limits | Not recorded |
| Dataset, row count, state, and seed history | Not recorded |
| API instances/processes | Not recorded |
| Effective pool size, overflow, and timeouts | Not recorded |
| Other effective non-secret settings | Not recorded |
| Background activity and other workloads | Not recorded |
| Warm-up, run order, pauses, and repetitions | Not recorded |

## Changes and constraints

- Files changed:
- Code, workload, or constraints changed:
- Reason:
- Shared interfaces preserved:
- Difference from the comparison run:

## Exact commands and evidence

Record start, validation, traffic, observation, and stop commands exactly as executed, including overrides and exit statuses. Reference raw summaries/logs if retained, without publishing secrets. Do not substitute planned commands for actual ones.

## Measured results

Add one column per run or repeat the table. Record units and the metric source.

| Measurement | Run value |
| --- | --- |
| Requested RPS and scheduling duration | Not recorded |
| Actual wall-clock/reporting duration | Not recorded |
| Total requests and achieved RPS | Not recorded |
| Successful requests / successful-work rate | Not recorded |
| Average latency | Not recorded |
| Median / P50 latency | Not recorded |
| P95 / P99 / maximum latency | Not recorded |
| Failed request count and rate | Not recorded |
| Error categories/statuses | Not recorded |
| Passed/failed checks and check definitions | Not recorded |
| Dropped iterations and interrupted work | Not recorded |
| Thresholds and test exit status | Not recorded |
| API CPU and memory | Not recorded |
| PostgreSQL CPU and memory | Not recorded |
| Load generator CPU and memory | Not recorded |
| Resource collection command/method, interval, timestamps | Not recorded |
| Snapshot, range, average, or measured peak | Not recorded |

CPU percentages do not directly measure remaining request capacity. Do not call a manual snapshot a peak or infer missing memory readings.

## Correctness evidence

- Expected versus actual endpoint status/body:
- Dataset invariants before and after:
- Automated checks, coverage, and gaps:
- Errors, interrupted runs, and unexpected changes:

## Observations

Only what the recorded evidence shows:

## Interpretation and alternative explanations

- Possible explanation:
- Other explanations compatible with the evidence:
- Comparison with a controlled earlier run:
- Evidence still needed to distinguish explanations:

## Limitations

Record missing telemetry, sample size, duration, shared resources, and why this does not establish universal or maximum capacity.

## Reset performed

- Exact stop/reset commands actually used:
- Configuration restored:
- Data retained or deliberately changed:
- Post-reset compatibility checks and results:

## Learning and next experiment

- What changed in my understanding:
- Questions still open:
- Next experiment and single factor to change:

## Future implementation details actually used

- Implemented endpoint, module, and load-test script:
- Enablement mechanism and proof of disabled default:
- Validated effective task settings:
- Distinct baseline/task engines and process count:
- Timing boundaries and instrumentation overhead:
- Server/client deadlines and retry behaviour:

## Pool-waiting measurements — only after implementation

| Measurement | 10 RPS run | 30 RPS run | 100 RPS run |
| --- | --- | --- | --- |
| Acquisition average/P50/P95, units | Not recorded | Not recorded | Not recorded |
| Query average/P50/P95, units | Not recorded | Not recorded | Not recorded |
| Holding time if instrumented | Not recorded | Not recorded | Not recorded |
| Pool timeouts | Not recorded | Not recorded | Not recorded |
| Statement timeouts | Not recorded | Not recorded | Not recorded |
| Client timeouts / other failures | Not recorded | Not recorded | Not recorded |
| Successful-work throughput | Not recorded | Not recorded | Not recorded |

Record missing query measurements on acquisition failure as unavailable, not successful zero-duration work. Record warm-up/connection creation separately where observable.

## Task-specific correctness and cleanup

- Disabled route and absence of task pool:
- Invalid configuration checks:
- Pool bound, zero overflow, and leak/cancellation checks:
- Error categorization and safe response bodies:
- Baseline compatibility before, enabled without task traffic, and after:
- Task engine cleanup and disabled state after reset:

Return to [Task 2](README.md).
