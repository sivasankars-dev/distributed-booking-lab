# Glossary

| Term | Meaning in this lab |
| --- | --- |
| API / endpoint | A program interface / one route such as `GET /events/1` |
| Baseline | Starting behaviour and measurements used for later comparisons |
| RPS | Requests per second; distinguish the requested rate from the achieved rate |
| QPS | Database queries per second; not necessarily equal to API RPS |
| Throughput | Work completed per unit of time; specify whether failures count |
| Concurrency | Work in progress at the same time; different from arrivals per second |
| Latency | Elapsed time for an operation; specify the measurement boundaries |
| Average | Sum of values divided by their count |
| Median / P50 | Value at or below which half the observations fall |
| P95 / P99 | Values at or below which about 95% / 99% of observations fall |
| HTTP status | Response classification such as success 200, missing resource 404, or unavailable 503 |
| k6 iteration | One execution of the load-test function; currently one HTTP event request |
| VU | Virtual user: a k6 worker that executes iterations |
| Arrival rate | How often new work is scheduled, independently of prior work finishing |
| Dropped iteration | Scheduled iteration the generator did not start; not a server response |
| Check | Assertion about a response, such as matching the requested event ID |
| Threshold | Test target; a failed k6 threshold makes the test unsuccessful |
| Health / readiness | Ability to respond / readiness check for a dependency; current readiness runs `SELECT 1` |
| Database connection | A conversation between the API and PostgreSQL |
| Connection pool | Reusable connections with a borrowing limit |
| Acquisition / checkout | Obtaining a connection from the pool; may include creating one |
| Holding time | Time from borrowing a connection until returning it |
| Pool waiting | Time waiting because a connection is not yet available |
| Overflow | Connections allowed above the pool's regular size; disabled in the starter |
| Pool timeout | Limit on waiting to acquire a connection |
| Statement timeout | Database limit on the execution of a statement |
| Client timeout | Limit on how long a client waits for a request |
| Async | Cooperative execution that can handle other work during I/O waits; not unlimited capacity |
| Saturation | A resource is sufficiently occupied that more arrivals cannot be served at the same pace |
| Backpressure | Slowing or limiting admitted work when downstream capacity is constrained |
| Retry | Another attempt after a failure; can add load and, for writes, correctness risks |
| Idempotency | Repeating an operation has the same intended effect as performing it once; not yet a booking feature here |
| Correctness | Required behaviour and data rules hold, beyond simply being fast |
| Observation / interpretation | Recorded evidence / a possible explanation of that evidence |
| Container / host | Isolated running environment / the computer whose resources it shares |
| Volume | Persistent container data storage; the database volume survives ordinary Compose shutdown |
| Commit / branch | Recorded Git revision / a named line of development; uncommitted work is not part of the commit |

Use [Task 1's concept guide](../labs/task-01-baseline/concept.md) and [Task 2's concept guide](../labs/task-02-pool-waiting/concept.md) for examples.
