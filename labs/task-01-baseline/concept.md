# Traffic, latency, and a baseline

A **baseline** is a starting measurement used for comparison. A **request** is one message to an API, such as `GET /events/1`. **Latency** is the time measured for that request. **Throughput** is work completed per unit of time. **RPS** means requests per second.

Think of a ticket-information desk. People arrive, wait, ask a question, and leave. Counting arrivals is different from timing their visit or counting completed visits. A desk may be quiet during one moment even though some visitors are waiting for information from another room.

## The concrete API path

k6 sends `GET /events/{id}`. FastAPI borrows a database connection, runs a query for that event ID, releases the connection, and returns the event. A connection is a reusable conversation with PostgreSQL; a pool holds a limited set of them. The request may spend time outside the SQL execution itself.

This exercise reads ticket availability; it does not reserve tickets. Two checks confirm HTTP 200 and the requested event ID. Manual checks cover sample ticket fields and the missing-event response.

## Requested traffic and achieved traffic

The script uses a constant-arrival-rate schedule: it tries to start a set number of iterations each second. An iteration is one execution of the script's request function. Here each iteration contains one event request, so 100 iterations per second targets 100 RPS.

A **virtual user (VU)** is a k6 worker that can run an iteration. This script preallocates 50 and permits at most 200. If an iteration takes longer, more workers may be needed to maintain arrivals. A **dropped iteration** is scheduled work k6 did not start, for example because no worker was available. It is not an HTTP error response; no request was sent for that dropped work.

Requested RPS is the configured arrival target. Achieved RPS is the request rate reported by k6's `http_reqs`. Scheduling boundaries and reporting duration can produce small differences even without failures. Examine totals, durations, completed iterations, and dropped work together. Do not divide by a guessed duration or call a low delivered rate proof that the API handled the requested load.

## Measurements

| Metric | Plain-English meaning and caution |
| --- | --- |
| Average | Sum of measured durations divided by their count; a few slow requests can pull it upward |
| Median / P50 | Half of measured durations are at or below this value |
| P95 | About 95% are at or below this value; it describes the slower part of the distribution, not the worst request |
| Maximum | Slowest measured request; one maximum does not establish a sustained problem |
| `http_req_duration` | k6 time sending, waiting for a response, and receiving; not SQL time alone and not connection establishment time |
| `http_req_failed` | k6's failed-request classification; by default expected HTTP statuses are 200–399, while transport errors also fail |
| Checks | Script assertions about responses; two per request here, reported separately from request failures |
| Dropped iterations | Scheduled iterations that did not start; exclude them from claims about successfully served traffic |
| CPU / memory | Resource readings at the observation time; state how and when collected |

An HTTP 200 response containing the wrong event ID can pass k6's HTTP-status failure classification and still fail the content check. An HTTP 404 is expected in the manual missing-event test, but would be unexpected for the seeded IDs in this load test.

A **threshold** is a test target whose failure makes k6 report an unsuccessful test. The script's thresholds are exercise choices. They do not establish a production service-level objective for a ticket sale.

## Facts, assumptions, and predictions

**Established from current code:** one API process; random event reads; two response checks; limited database pool; no booking writes in this workload.

**Assumptions to verify locally:** seed data is intact, no other load test is running, effective pool size matches your note, and Docker has the resources you recorded.

**Predictions to test:** raising traffic might increase latency, produce waiting, or show little change within this range. Lower latency in a later run might involve warm caches or ordinary variation; those explanations require further experiments.

Your hardware, Docker settings, workload, and background activity affect results. Published measurements are examples, not scores to match. CPU percentages do not directly measure remaining request capacity, and low CPU does not rule out waiting. Record observations separately from explanations and change one factor at a time.

Return to [Task 1](README.md) or consult the [glossary](../../docs/glossary.md).
