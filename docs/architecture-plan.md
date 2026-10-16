# Future architecture plan

**Plan only: these Python files and the Task 2 endpoint have not been created by this documentation change.** Current runtime code remains in [app/main.py](../app/main.py). Extract only what a concrete implementation needs; do not build a framework for every possible future task.

## Proposed organization

```text
app/
  main.py
  core/
    config.py
    database.py
  routers/
    health.py
    events.py
  tasks/
    task_02_pool_waiting/
      __init__.py
      router.py
```

This shows proposed responsibilities, not an available import layout. Add package initialization only as required when implementing real modules.

| Proposed location | Responsibility |
| --- | --- |
| `app/main.py` | Compose the application, preserve timing middleware, register baseline routes, conditionally register enabled task routes, coordinate startup/shutdown |
| `app/core/config.py` | Read and validate concrete shared and task-specific settings; keep defaults compatible; reject invalid enabled configuration |
| `app/core/database.py` | Manage actual engine creation/cleanup needed by implemented tasks; preserve the baseline engine and keep task engines separate |
| `app/routers/health.py` | Preserve `/health` and `/ready` contracts, with readiness using the baseline database connection path |
| `app/routers/events.py` | Preserve event lookup, parameterized query, response shape, and missing-event 404 |
| `app/tasks/task_02_pool_waiting/__init__.py` | Package boundary, without import-time creation of pools or background work |
| `app/tasks/task_02_pool_waiting/router.py` | Task-only route and experiment observations using the dedicated task pool |

## Configuration and lifecycle

Task 2's [future implementation contract](../labs/task-02-pool-waiting/README.md#implementation-steps--future-work) proposes validated `TASK_02_*` settings. They must not alter `DB_POOL_SIZE` or baseline timeouts. Wiring into Compose and a populated `.env.example` is future implementation work; a setting is not available merely because it is documented.

When disabled, do not register the experimental route or allocate a task engine. When enabled, validate settings before accepting traffic and create a distinct task engine with bounded pool size, zero overflow, and task-specific statement timeout. Do not change a shared session's settings to simulate task behaviour.

Coordinate lifespan cleanup for every engine that was successfully created, including partial startup failure. Ensure request success, exception, timeout, and cancellation release or safely discard connections. Shutdown must dispose of task and baseline engines and document how pending work is handled.

## Compatibility and resources

Preserve the starter's interfaces and default launch/load-test commands during extraction. Confirm Task 1's health, readiness, event, missing-event, and data checks before and after changes, with the task both disabled and enabled without task traffic. Add tests for configuration validation, endpoint outcomes, timing boundaries, and lifecycle cleanup when implementing those behaviours.

Separate modules support code organization; separate pools prevent Task 2 from checking out baseline pool connections. Neither reserves PostgreSQL CPU, memory, I/O, host capacity, or the server's total connection budget. Each API process would own its own engines and pools. Budget the combined connections when exploring multiple processes later.

Run experiments sequentially unless interference is the explicit subject. Record background work and return to a quiet baseline before comparison. Avoid changing shared defaults to make one lesson demonstrate a desired failure.

## Longer-term learning goals

The existing project ambition includes studying workloads associated with millions of daily active users and peaks around 5,000 RPS. These remain learning goals, not verified capacity. Daily users, API request rate, and database query rate are different measurements. Any future capacity claim needs a defined workload, hardware, configuration, duration, and correctness evidence.

## What to defer

Do not create generic plugin registries, speculative pool managers, or empty task modules now. Extract reusable logic when a concrete second use requires it. Booking writes, queues, caching, and multiple replicas remain future lessons with their own correctness and resource requirements.
