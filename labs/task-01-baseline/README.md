# Task 01 — Event API baseline

## Production scenario

Before a ticket sale, an engineer needs evidence about event-page reads. A fast response is useful only if it contains the correct event. This exercise establishes a read-only baseline; it does not measure reservation or payment capacity.

## Learning outcomes

Distinguish requested traffic from achieved traffic, interpret latency and errors together, inspect response correctness, observe container resources, and record evidence that another learner can understand.

## Prerequisites

Complete [Start Here](../../docs/start-here.md). Have Docker Desktop, Compose, and curl available, port 8000 free, and the seeded dataset. Know how to run a terminal command and read an HTTP status.

## Current readiness status

**Ready to try.** Instructions match the existing application and baseline script. No runtime verification was performed as part of publishing these documents. Historical runs are linked in [learning notes](../../docs/learning-notes/README.md).

## Concept document

Read [Traffic, latency, and a baseline](concept.md), especially requested versus achieved RPS and the limits of the checks.

## Starting state

One API process and PostgreSQL 16, with 10,000 events (`id` 1–10000), each initially containing 1,000 total and available tickets. Default API pool capacity is 5 with no overflow. Confirm actual configuration and data; existing volumes may differ from the seed.

## Files the learner may change

For the initial experiment, change only your own note under `docs/learning-notes/<name>/`. Use [loadtests/baseline.js](../../loadtests/baseline.js) in place; do not move, duplicate, or edit it for the baseline. Traffic changes use existing `RATE` and `DURATION` inputs. Later question challenges belong on a separate practice branch and must record any code change.

## Shared interfaces and baseline behaviour to preserve

Preserve `/health`, `/ready`, and `/events/{event_id}`, including response bodies, event-ID matching, and missing-event HTTP 404. Do not change application code, seed SQL, runtime configuration, or load-test behaviour for the initial measurements. These reads must not change ticket counts.

## Prediction

Before each run, predict achieved RPS, average/P50/P95 latency, failures, checks, dropped iterations, and resource changes. Explain what evidence would contradict your prediction. Do not assume latency must rise as the requested rate rises.

## Experiment steps

1. Record your environment, commit, working-tree changes, and effective configuration using the [results template](results-template.md).
2. Start containers and check all four endpoint behaviours below. Confirm seed data; stop and investigate mismatches before loading the API.
3. Run 50, 100, and 300 RPS sequentially, initially for 30 seconds each. Record order, pauses, and any warm-up. Do not run another experiment concurrently.
4. Watch CPU and memory in a second terminal. Save k6 summaries and note the resource collection method.
5. Optionally repeat 300 RPS for 60 seconds, then repeat earlier rates to investigate run-order effects. Record every run, including failures.
6. Repeat endpoint and dataset checks. Separate observations from possible explanations and limitations.

## Execution commands

Run from the repository root:

```bash
docker compose up --build -d
docker compose ps
curl -i http://localhost:8000/health
curl -i http://localhost:8000/ready
curl -i http://localhost:8000/events/1
curl -i http://localhost:8000/events/10001
```

| Request | Expected result with seeded data |
| --- | --- |
| `/health` | HTTP 200, `{"status":"ok"}`; no database query |
| `/ready` | HTTP 200, `{"status":"ready"}` when `SELECT 1` succeeds; HTTP 503 on a caught database-check error |
| `/events/1` | HTTP 200, `{"id":1,"name":"Learning Event 1","total_tickets":1000,"available_tickets":1000}` |
| `/events/10001` | HTTP 404, `{"detail":"Event not found"}` |

`curl -i` shows status, headers, and body; inspect them. Curl completing does not mean the response matched expectations. The API timing middleware adds `X-Response-Time-Ms`, but this is not a separate measurement of connection waiting or query duration.

Use this read-only dataset check before and after the experiment:

```bash
docker compose exec db psql -U lab -d booking_lab -c 'SELECT count(*) AS event_count, min(id) AS first_id, max(id) AS last_id, count(*) FILTER (WHERE total_tickets <> 1000 OR available_tickets <> 1000) AS changed_ticket_rows FROM events;'
```

For unchanged seed data expect `10000`, `1`, `10000`, and `0`. This is a sample invariant check, not proof that every field and business rule is correct.

In a second terminal, start resource observation before each load test:

```bash
docker stats
```

Record API, database, and load-generator CPU and memory values, sampling times, and whether values are snapshots, ranges, or measured peaks. Ctrl+C stops the viewer. `docker stats --no-stream` gives a single snapshot; it cannot establish a run's peak. Include the load generator because it competes for host resources and may limit delivered traffic.

In the first terminal, run one command at a time and retain each complete summary and exit status:

```bash
RATE=50 DURATION=30s docker compose --profile tools run --rm loadtest
RATE=100 DURATION=30s docker compose --profile tools run --rm loadtest
RATE=300 DURATION=30s docker compose --profile tools run --rm loadtest
```

Optional longer run:

```bash
RATE=300 DURATION=60s docker compose --profile tools run --rm loadtest
```

Explicit rate/duration values prevent a local `.env` from silently changing these runs. k6 schedules arrivals for that duration; startup and completion of outstanding work can make wall-clock time longer. A nonzero exit status may indicate a threshold failure: retain the output and investigate.

## Measurements and correctness checks

Read [the metric definitions](concept.md#measurements) before interpreting the output. Record requested and achieved RPS, total requests, average, median/P50, P95, maximum, `http_req_failed`, checks, and dropped iterations. Record P99 only if collected; the default summary need not contain it.

The script requests uniformly random IDs from 1–10000, with one HTTP request per iteration, 50 preallocated virtual users and a maximum of 200. Its two checks are HTTP 200 and matching event ID. They do not validate all response fields or booking correctness. A successful HTTP request can still fail a content check.

Current thresholds are P95 < 300 ms, request failure rate < 1%, check pass rate > 99%, and exactly zero dropped iterations. These are strict exercise thresholds from the script, not measured guarantees or universal production requirements. A threshold failure is evidence to investigate, not permission to hide a run.

Confirm the manual endpoint and SQL checks still match afterwards. Inspect `docker compose logs --tail=100 api db` for errors if needed. The baseline does not measure pool acquisition and query execution separately; do not attribute all latency to SQL.

## Completion criteria

Record all three rates with exact commands, actual results, correctness checks, resource observations or explicit missing values, and limitations. Explain at least one alternative interpretation. A well-documented run that fails a target still completes the learning exercise; resolving the failure can become the next experiment. Do not infer maximum capacity from the highest tested rate.

## Reset instructions

Allow the active test to finish or stop its foreground process with Ctrl+C and mark it as interrupted. Check `docker compose ps -a`; if an interrupted load-test container remains active, stop the load-test service with `docker compose --profile tools stop loadtest`. Stop log/resource viewers separately. `--rm` removes completed one-off load-test containers.

Use `docker compose down` to stop the application while retaining data. Restart with `docker compose up -d`. No dataset reset is needed for these reads. Remove temporary shell overrides you introduced and record any local configuration changes; do not delete `.env` or database volumes blindly. Recheck health, readiness, event lookup, and missing-event behaviour before another experiment.

## Questions document

Try [Easy, Medium, and Hard questions](questions.md). Challenges beyond the initial baseline are clearly labeled.

## Results template

Copy [the baseline results template](results-template.md) into your own learning-note file. Keep [Siva's historical report](../../docs/learning-notes/siva/task-01-baseline.md) unchanged.
