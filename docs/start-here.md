# Start here

This lab uses event reads as the foundation for learning booking-system behaviour. You are not making reservations yet. Read [Task 1](../labs/task-01-baseline/README.md), make a prediction, and record your own measurements before comparing them with published examples.

## What runs today

| File | Responsibility |
| --- | --- |
| [app/main.py](../app/main.py) | FastAPI routes, response timing, and database engine lifecycle |
| [db/init.sql](../db/init.sql) | Events table and 10,000 initial rows |
| [compose.yaml](../compose.yaml) | API, PostgreSQL, and optional k6 container |
| [Dockerfile](../Dockerfile) | Builds the API image and starts one Uvicorn process |
| [loadtests/baseline.js](../loadtests/baseline.js) | Random event reads at a requested arrival rate |

The API listens on `127.0.0.1:8000` on your computer. The load-test container uses `http://api:8000` on the Compose network. PostgreSQL has no published host port. Containers still share your computer's resources.

## Requirements and setup

You need Git, Docker Desktop with Docker Compose, a running Docker daemon, and `curl`. Commands use macOS/Linux shell syntax. After cloning, run the remaining commands from the repository root. Image builds and pulls may need network access. You do not need a host Python installation or host k6 installation for these commands.

Clone the repository and enter its directory. If you already have a checkout, open its directory instead.

```bash
git clone https://github.com/sivasankars-dev/distributed-booking-lab.git
cd distributed-booking-lab
```

Start the application:

```bash
docker compose up --build -d
docker compose ps
docker compose logs --tail=100 api db
```

The first startup may take time. Check readiness before generating traffic. [Task 1's endpoint checks](../labs/task-01-baseline/README.md#execution-commands) include expected bodies and missing-event behaviour.

```bash
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/ready
```

`/health` returns `{"status":"ok"}` without querying PostgreSQL. `/ready` runs `SELECT 1`: success returns `{"status":"ready"}`, and a caught database-check error returns HTTP 503 with `{"detail":"Database unavailable"}`. Readiness does not prove that the events table has the expected dataset.

## Configuration today

The current starter works without `.env`: Compose provides local database credentials and defaults. A documented `.env.example` is planned.

Compose reads a local `.env` for variable substitution. Only settings wired through Compose reach the relevant container; arbitrary entries do not configure the application automatically. Shell values take precedence over `.env` substitution for the variables below.

| Setting | Current default | Effect |
| --- | --- | --- |
| `DB_POOL_SIZE` | `5` | API pool capacity per process; applied when API starts |
| `RATE` | `50` | k6 scheduled iterations per second; one event request per iteration |
| `DURATION` | `30s` | k6 arrival-scheduling duration |
| `BASE_URL` | Compose fixes `http://api:8000` | k6 destination; a host `.env` value does not override this literal |
| `DATABASE_URL` | Compose supplies the local `booking_lab` connection | API database; a host `.env` value does not override this literal |

Current API constants are no overflow connections, a 2-second pool acquisition timeout, and a 3,000 ms PostgreSQL statement timeout. These are not currently environment settings. Pool connections open as needed; capacity is not proof that all connections are already open. Keep defaults for the first baseline and record any effective differences.

To inspect the running pool-size setting without printing credentials:

```bash
docker compose exec api printenv DB_POOL_SIZE
```

A local `.env` is ignored by Git, but it does not automatically secure secrets. The supplied credentials are for local learning. Do not publish secret values in results or configuration dumps. Record the effective non-secret configuration instead.

## Record before running

```bash
git branch --show-current
git rev-parse HEAD
git status --short
docker version
docker compose version
```

Record CPU, RAM, OS, Docker CPU/memory limits, other running workloads, date/timezone, dataset state, and uncommitted changes in the task's template. A commit alone does not describe a dirty working tree. Use `Not recorded` when evidence is missing.

## Stop, restart, and data

```bash
docker compose down
docker compose up -d
```

Stopping this way retains the named PostgreSQL volume. The seed SQL runs only on initialization of an empty volume; restarting does not restore edited data. Task 1 is read-only and needs no data deletion. Do not delete volumes to troubleshoot without first deciding whether their data can be lost.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Docker cannot connect | Start Docker Desktop and inspect its status |
| Port 8000 is occupied | Identify and stop your conflicting local service before retrying |
| API not ready | `docker compose ps` and `docker compose logs --tail=100 api db` |
| Event checks fail | Confirm readiness, seed row count, and event response fields |
| k6 fails a threshold | Inspect failures, individual checks, latency, and dropped iterations together |
| Results differ from Siva's | Compare hardware, effective configuration, workload, duration, and background activity |

For live logs use `docker compose logs -f api db`; Ctrl+C exits the viewer without stopping containers. For terms see the [glossary](glossary.md). For branches see [contributing tasks](contributing-tasks.md).
