# Connections, holding time, and waiting

**Status: Planned — requires application implementation before running.** This explains the proposed exercise; the starter has no slow-query endpoint or separate timing observations.

## An everyday analogy

Imagine five ticket-desk phones. An employee must borrow a phone to call the inventory office. If all five are in use, the next employee waits. A call can keep a phone occupied even while nobody is speaking. Adding more people to the desk does not create more phones or make the inventory office faster.

## Connections and pools

A **database connection** is a conversation between the application and PostgreSQL. A **connection pool** keeps reusable connections and limits how many can be borrowed. Borrowing is often called **acquisition** or **checkout**; returning a connection makes it available to another request.

**Connection holding time** is how long a request keeps its connection before returning it. It includes work performed while holding the connection, not only time the database CPU is busy.

In the current event endpoint, a request obtains a connection, runs a lookup, and releases it. In the proposed task endpoint, a request would obtain a separate task-pool connection and ask PostgreSQL to sleep briefly before releasing it.

## Waiting is different from execution

**Pool waiting** occurs when a request cannot yet borrow a connection because the allowed connections are occupied. A **pool timeout** limits how long acquisition can wait before failing. A **statement timeout** limits database statement execution. A **client timeout** limits how long the load-test client waits. These limits cover different intervals.

A request can wait for a connection before its query even begins. The overall response can therefore take much longer than the query. Measure acquisition and query durations separately. Acquisition can also include establishing a new connection, and query duration can include network and driver overhead; name observations accurately.

For example, an availability request might take a long time to acquire a connection and then execute its query quickly. That is different evidence from quick acquisition followed by a long query. Today's starter does not expose these two timings separately.

## Why async does not remove limits

**Async execution** lets the API attend to other requests while one is waiting for I/O, such as a database response. It does not create additional PostgreSQL capacity or free a connection that a pending operation still holds. Many waiting requests can accumulate while the process does little CPU work.

Low CPU therefore does not rule out pool waiting, lock waiting, or other blocked work. CPU percentages do not directly measure remaining request capacity. Memory, latency, timeouts, and delivered traffic also matter.

## A small capacity estimate

Assume a task-specific pool of 5 connections, zero overflow, one connection per request, and about 100 ms (`0.1` seconds) holding time:

```text
idealized service rate = connections / holding time
                      = 5 / 0.1
                      ≈ 50 requests per second
```

This is an idealized estimate before overhead, not a measured guarantee. Actual holding time, connection creation, scheduling, PostgreSQL contention, and other resources can change the result. Five is the proposed per-process task-pool limit, not a total database connection budget.

The proposed 10 and 30 RPS tests are below that estimate; 100 RPS is above it. Whether and when waiting or timeouts appear is a prediction to test. Finite runs, generator limits, and quickly rejected requests complicate achieved-RPS interpretation. Record successful work separately from all HTTP responses.

## What the simulation models

PostgreSQL's `pg_sleep` pauses the database session for a requested interval while the application holds its connection. The proposed default is approximately 100 ms. Use this to study connection occupancy without needing a complex dataset or an intentionally expensive query.

It does not reproduce every slow production query. It is not a model of all CPU-heavy joins, disk reads, lock contention, query plans, or index problems. PostgreSQL sleeping while CPU stays low is compatible with a pool becoming busy. Do not conclude that production queries should be fixed only by increasing pool size.

## Facts, assumptions, and predictions

**Established facts:** a bounded pool limits concurrent borrowers; waiting for a connection precedes execution; separate pools still share database and host resources; async does not make those resources unlimited.

**Exercise assumptions:** one process, a dedicated pool of 5, no overflow, approximately 100 ms holding time, and sequential tests. Verify them in your future implementation and record effective settings.

**Predictions:** waiting may rise when arrivals exceed sustainable service; failures may appear when deadlines expire. Results depend on your machine, run duration, configuration, and workload. These are hypotheses, not published measurements.

Return to [Task 2](README.md) or review the [glossary](../../docs/glossary.md).
