# Experiment Record

> **Run these experiments on your own device.**
>
> The results below were collected on Siva's computer. Your results may differ because of your CPU, memory, Docker settings, background applications, and software versions.
>
> Even repeated tests on the same computer may produce different results. Use these measurements as examples, not as scores to match. Test your device, observe the behaviour, and record what you learn.

## Experiment 01: Event API Baseline

### Goal

Understand how the event API behaves when request traffic increases.

A baseline is the starting measurement used to compare future changes.

### Hypothesis

Increasing traffic may increase latency if requests start waiting for application or database resources.

If sufficient resources are available, higher traffic may not significantly increase latency.

### Test Environment

| Setting | Value |
| --- | --- |
| Learner | Siva |
| Test date | 2026-10-16 |
| Computer | MacBook Pro; exact specifications not recorded |
| OS version | Not recorded |
| Git commit used during tests | Not recorded |
| Docker resource limits | Not recorded |
| Dataset | 10,000 events |
| API processes | 1, based on starter configuration |
| Database | PostgreSQL 16 |
| Database pool size | Default: 5; effective value not independently recorded |
| Endpoint | `GET /events/{id}` |
| Deployment | API, database, and load generator on the same computer |

Missing historical values should remain `Not recorded` unless they can be confirmed.

## Changes Between Runs

| Run | Requested RPS | Duration | Change |
| --- | ---: | ---: | --- |
| 1 | 50 | 30 seconds | Initial baseline |
| 2 | 100 | 30 seconds | Increased request rate |
| 3 | 300 | 30 seconds | Increased request rate |
| 4 | 300 | 60 seconds | Increased test duration |

No application code changes were reported between these runs.

## Commands Used

Start the application:

```bash
docker compose up --build -d
```

### Run 1: 50 RPS for 30 seconds

```bash
docker compose --profile tools run --rm loadtest
```

This run used the starter defaults of 50 RPS and 30 seconds.

### Run 2: 100 RPS for 30 seconds

```bash
RATE=100 DURATION=30s docker compose --profile tools run --rm loadtest
```

### Run 3: 300 RPS for 30 seconds

```bash
RATE=300 DURATION=30s docker compose --profile tools run --rm loadtest
```

### Run 4: 300 RPS for 60 seconds

```bash
RATE=300 DURATION=60s docker compose --profile tools run --rm loadtest
```

Observe resource usage in another terminal:

```bash
docker stats
```

## Results

| Metric | Run 1 | Run 2 | Run 3 | Run 4 |
| --- | ---: | ---: | ---: | ---: |
| Requested RPS | 50 | 100 | 300 | 300 |
| Duration | 30 s | 30 s | 30 s | 60 s |
| Total requests | 1,500 | 3,001 | 9,001 | 18,001 |
| Achieved RPS | 50.00 | 100.02 | 299.99 | 300.01 |
| Average latency | 3.47 ms | 2.60 ms | 1.44 ms | 1.39 ms |
| P50 latency | 3.56 ms | 2.57 ms | 1.31 ms | 1.32 ms |
| P95 latency | 5.10 ms | 3.94 ms | 1.88 ms | 1.82 ms |
| Maximum latency | 33.51 ms | 63.15 ms | 46.13 ms | 48.89 ms |
| Failed requests | 0 | 0 | 0 | 0 |
| Checks passing | 100% | 100% | 100% | 100% |
| Dropped iterations | 0 | 0 | 0 | 0 |

P99 was not included in the supplied test summaries.

## Understanding the Measurements

| Measurement | Meaning |
| --- | --- |
| RPS | API requests per second |
| Average latency | Average time taken by a request |
| P50 latency | 50% of requests completed within this time |
| P95 latency | 95% of requests completed within this time |
| Maximum latency | Time taken by the slowest measured request |
| Failed requests | Requests counted as failures by k6 |
| Checks | Validation of response status and event ID |
| Dropped iterations | Scheduled work that k6 could not start |

The latency values use k6's `http_req_duration`. They do not measure database query time alone.

Each request has two checks:

1. Did the API return HTTP 200?
2. Did the response contain the requested event ID?

For example, Run 4 completed 18,001 requests and passed 36,002 checks.

## Resource Observations

During Run 4, the following approximate CPU values were observed manually:

| Container | Observed CPU usage |
| --- | ---: |
| API | Around 39% |
| PostgreSQL | Around 12% |
| Load generator | Around 26% |

Memory usage was not recorded.

These are manually observed values, not continuously recorded peaks.

**CPU usage is not the percentage of maximum request capacity.** An API CPU reading of 39% does not mean that 61% of request capacity remains.

## Observations

- All runs achieved approximately the requested request rate.
- No request failures were reported.
- No iterations were dropped.
- All response checks passed.
- Average and P95 latency were lower in later runs.
- The 300 RPS results were similar for 30-second and 60-second tests.
- Maximum latency varied between runs.

## Interpretation

The event API handled the tested workloads successfully.

Increasing traffic from 50 to 300 RPS did not increase average or P95 latency in these runs.

Cache warming and normal run-to-run variation are possible explanations for the lower latency. These measurements do not confirm the exact cause.

A higher maximum latency alone does not prove sustained performance degradation.

## Limitations

- Maximum system capacity has not been identified.
- These results do not establish support for 5,000 RPS.
- A 60-second test does not establish long-term reliability.
- The workload reads events; it does not test booking writes or payment processing.
- The API, database, and load generator share the same computer.
- Each rate and duration combination was tested once.
- Database query time and connection-pool waiting were not measured separately.
- Response checks validate status and event ID, not every business rule.

## What I Learned

- RPS and concurrent requests measure different things.
- More traffic does not always cause proportionally higher latency.
- Average, percentiles, failures, and dropped work should be examined together.
- CPU usage helps investigation but does not identify a bottleneck alone.
- Observations and possible explanations should be recorded separately.

## Next Experiment — Planned

Introduce a controlled slow-query scenario in an isolated task module.

Investigate how connection holding time and pool size affect:

- Request waiting
- Response latency
- Request failures
- Application and database resource usage

Keep experimental behaviour disabled by default and preserve the existing baseline endpoint.

## Record location

This historical report was moved from `docs/experiments.md` without changing its recorded measurements, observations, or interpretations. Test time/timezone, uncommitted changes, and raw-output artifacts were not recorded in the supplied report; do not infer them from the migration date or current repository state.

For a new experiment, use your own note and the [Task 1 results template](../../../labs/task-01-baseline/results-template.md). See the [learning-notes index](../README.md).
