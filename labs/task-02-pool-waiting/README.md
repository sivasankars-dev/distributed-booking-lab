# Task 02 — Slow database work and pool waiting

## Production scenario

During a popular ticket sale, an availability request holds a database connection longer than usual. New requests wait even though API CPU looks low. You need to distinguish time spent obtaining a connection from time spent using it before choosing a remedy.

## Learning outcomes

Explain connection holding time and pool capacity, measure acquisition and query durations separately, investigate overload and timeouts, and preserve the baseline while introducing a controlled experiment.

## Prerequisites

Complete [Task 1](../task-01-baseline/README.md) and retain your results. You need basic async Python, FastAPI, SQLAlchemy lifecycle handling, PostgreSQL, and k6 knowledge. Learn unfamiliar terms in the concept guide before implementing. This task requires writing and validating application code on your own practice branch.

## Current readiness status

**Planned — requires application implementation before running.**

Only this exercise specification exists. The endpoint, task pool, configuration, instrumentation, and dedicated load test described below are future implementation details. No Task 2 command or proposed setting works in the current starter. No Task 2 measurements have been collected here.

## Concept document

Read [Connections, holding time, and waiting](concept.md).

## Starting state

The current application has one shared engine in `app/main.py`. Health, readiness, and event routes exist; a slow-query route does not. Task 1's `loadtests/baseline.js` must stay unchanged. Refer to the [future architecture plan](../../docs/architecture-plan.md) for organization, not existing files.

## Files the learner may change

For future implementation on a practice branch, the proposed module is `app/tasks/task_02_pool_waiting/router.py`, with package initialization in `app/tasks/task_02_pool_waiting/__init__.py`. Task-specific configuration and lifecycle integration may require careful edits to `app/main.py` and, when extraction is justified, the proposed `app/core/config.py` and `app/core/database.py`.

Proposed load-test file: `loadtests/tasks/task-02-pool-waiting.js`. Future Compose wiring may be needed to pass task settings and select that script explicitly. Add meaningful tests when implementing. Record every changed file. Do not create placeholders as evidence that the task works, or change the shared baseline pool to reproduce the task's failure.

## Shared interfaces and baseline behaviour to preserve

Preserve `/health`, `/ready`, `/events/{event_id}`, seed data, default pool settings, response bodies, missing-event 404, and the existing baseline script/command. Task 2 must use a separate engine/pool, with no borrowing from the baseline pool. It must not write events or change ticket counts.

Separate modules and pools are not complete runtime isolation. They share PostgreSQL connection limits, database CPU/memory, and the host with the generator. Multiple API processes would each own pools. Run baseline and Task 2 experiments sequentially unless deliberately studying interference.

## Prediction

Assume one process, a task-specific pool of 5, no overflow, one connection per request, and approximately 100 ms holding time per successful request. The idealized estimate `5 / 0.1 ≈ 50 requests per second` is before overhead, not a measured guarantee.

Predict waiting, query duration, latency, successful throughput, timeouts, and dropped work at 10, 30, and 100 RPS. Explain which assumptions might fail. Do not assume total HTTP throughput equals successful database-work throughput when requests can fail quickly.

## Implementation steps — future work

All names and settings in this section are **proposed future implementation details**, not current configuration.

### Endpoint contract to implement

Proposed route: `GET /tasks/pool-waiting/slow-query`. Keep the simulated work duration in validated configuration rather than accepting arbitrary SQL or unbounded delays from callers.

On successful completion, return HTTP 200 with an explicit success status and observations such as proposed `pool_acquire_ms` and `query_ms` fields. Use a stable, documented response schema so the future load test can verify it. The endpoint should perform one parameterized PostgreSQL `pg_sleep` operation while holding a task-pool connection. Approximately 100 ms is the default target, not an exact response-time guarantee.

Map pool-acquisition timeout to a documented HTTP 503 error (proposed error code `pool_timeout`). Distinguish database statement timeout (proposed `query_timeout`) and database unavailability (proposed `database_unavailable`) using documented HTTP 503 responses and structured logs. Do not expose credentials or raw database errors. Do not report failed work as successful. Unexpected programming errors should remain visible as failures, not be mislabeled as capacity timeouts.

### Configuration and validation to implement

| Proposed future setting | Proposed default | Required validation/behaviour |
| --- | --- | --- |
| `TASK_02_ENABLED` | `false` | Strict boolean parsing; when disabled, do not register the task route or create its pool; route returns normal 404 |
| `TASK_02_POOL_SIZE` | `5` | Integer within a documented safe local bound, proposed 1–20; independent of `DB_POOL_SIZE` |
| `TASK_02_WORK_MS` | `100` | Finite positive duration, proposed 1–1000 ms; reject invalid values at startup when enabled |
| `TASK_02_POOL_TIMEOUT_SECONDS` | `2` | Finite positive value, proposed at most 10 seconds; bounds connection-acquisition waiting |
| `TASK_02_STATEMENT_TIMEOUT_MS` | `1000` | Positive integer greater than configured work duration, proposed at most 5000 ms; bounds SQL execution |

These values are exercise design choices. The task pool must have zero overflow connections and use task-specific database session settings. Invalid enabled configuration should fail startup clearly, not silently fall back or partly activate. Keep disabled mode compatible with the starter. Future `.env.example` entries and Compose wiring must agree with what the application actually reads; adding a host variable alone is insufficient.

Choose and document a load-test request timeout that allows you to observe intended server timeouts, plus a bounded allowance for overhead. Explain the order of pool, statement, and client deadlines; do not assume one timeout bounds the entire request. Automatic retries are not part of the initial experiment.

### Timing observations to implement

Use a monotonic clock, which measures elapsed time without being affected by wall-clock corrections. Measure acquisition from just before requesting a connection until it is obtained, and query duration from executing the sleep statement until completion. Release the connection on success, timeout, exception, and cancellation.

Acquisition duration can include opening a new physical connection, especially during startup; do not label every millisecond as queue waiting. Record cold versus warmed runs. Query duration includes the database/driver round trip and sleep, not only PostgreSQL CPU execution. Also record connection holding time through release where practical and overall request duration separately.

Expose measurements on successful responses and in structured logs or metrics for failed attempts, with failure category and request correlation. An acquisition timeout has a measured wait but no executed query; record query duration as unavailable, not zero successful work. The current `X-Response-Time-Ms` header alone cannot provide this breakdown. The dedicated load test should collect distributions and outcome counts without relying only on averages.

### Load test to implement

Implement the proposed dedicated script with one task request per iteration, a constant arrival rate, explicit request timeout, response-schema checks, separate success/timeout counts, and acquisition/query timing collection. Document virtual-user limits and experiment thresholds. Select this script explicitly through future tooling; the existing Compose load-test command still runs the baseline script.

After correctness validation, run 10, 30, and 100 RPS sequentially, initially for a proposed 30 seconds per run. Record duration, warm-up, effective configuration, and all thresholds actually used. Preserve failures and dropped iterations. Do not change several limits simultaneously to obtain a preferred result.

## Execution commands

**No runnable Task 2 commands are available yet.** Implement and test the runtime pieces, then add exact enable/start, script-selection, load-test, and disable commands to this section. Do not run baseline traffic while calling it a slow-query experiment.

Today you can run [Task 1's commands](../task-01-baseline/README.md#execution-commands) to establish compatibility evidence, inspect code, and write predictions. The future rate values and configuration table above describe the intended experiment only.

## Measurements and correctness checks

Before load testing a future implementation, verify:

- Disabled mode returns 404 for the task route and creates no task engine; enabled mode uses an engine distinct from the baseline engine.
- Invalid enabled settings fail validation. The default task pool allows at most 5 checked-out connections with no overflow.
- Successful responses represent completed work; their timing fields have documented units and sensible nonnegative values.
- Acquisition timeouts do not execute the query. Query timeouts and database failures have distinguishable outcomes. Cancellation and errors return/discard connections correctly, with no leak across repeated runs.
- Baseline health, readiness, event lookup, missing-event response, and dataset checks pass with the feature disabled and again after enabling it without task traffic.
- After task traffic stops and outstanding work settles, repeat baseline checks and a sequential baseline load run. Record interference or changed latency without assuming identical performance.

At each rate collect requested/achieved traffic, total and successful requests, latency average/P50/P95, errors by category, checks, dropped iterations, acquisition/query duration distributions, and API/database/generator CPU and memory. Connection occupancy or queue depth would require additional instrumentation; do not claim those measurements exist today.

## Completion criteria

The future implementation must satisfy the disabled-by-default, validation, isolation, response, timing, cleanup, and compatibility requirements above. Record all three load levels, correctness evidence, exact commands, changes, limitations, and alternative explanations. Keep the status Planned until runtime pieces and usable commands exist. Mark a revision Verified only with actual recorded execution evidence.

## Reset instructions

Future implementation must document how to stop its dedicated load generator, let outstanding work finish or cancel safely, disable the feature, and restart/recreate the API so the running configuration changes. Dispose of the task engine at shutdown; do not leave sessions or transactions checked out.

Task 2 should not mutate persistent data, so volume deletion is not a reset requirement. Remove only task-specific temporary artifacts/settings you introduced. Verify the task route is unavailable after disabling, task connections are cleaned up, and Task 1's endpoints/data still behave correctly. `docker compose down` remains the existing way to stop the current stack while retaining its database volume; task-specific cleanup commands remain to be implemented and documented.

## Questions document

Explore [Easy, Medium, and Hard questions](questions.md) after writing predictions. Advanced challenges extend the exercise and are not implemented solutions.

## Results template

Use [the pool-waiting results template](results-template.md). Until you implement and run this task, record predictions and unavailable measurements explicitly; do not fill the table with estimates as if they were results.
