# Distributed Booking Lab

Learn distributed systems through a local booking application: understand a concept, predict behaviour, run an experiment, check correctness, and explain the evidence. This is for beginners with basic Python, HTTP, SQL, and terminal knowledge who want practical engineering experience, including production problems.

## Current functionality

The starter has one FastAPI process, PostgreSQL 16, 10,000 seeded events, event lookup, health/readiness checks, a configurable connection pool, and a k6 baseline load test. Booking writes, payments, caching, queues, and multiple API instances are not implemented.

## Quick start

With Docker Desktop running and Docker Compose installed, run from this repository's root:

```bash
docker compose up --build -d
docker compose ps
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/ready
curl --fail http://localhost:8000/events/1
```

The starter works without `.env`. See [Start Here](docs/start-here.md) for configuration, expected responses, troubleshooting, and stopping the application. Interactive API documentation is at <http://localhost:8000/docs>.

## Tasks

| Task | Readiness |
| --- | --- |
| [01 — Baseline](labs/task-01-baseline/README.md) | Ready to try |
| [02 — Pool waiting](labs/task-02-pool-waiting/README.md) | Planned — requires application implementation before running |

The [task index](labs/README.md) explains readiness labels. The baseline instructions match existing code; this documentation change does not establish runtime verification.

## Learning workflow

Read the concept → predict → implement when required → experiment locally → inspect evidence and correctness → explore questions → record findings. Each task has a concept guide, questions without answers, and a results template.

Results vary by hardware, configuration, workload, and background activity. Test your own device; published results are examples, not scores to match. Separate observations from possible explanations. CPU percentages do not directly measure remaining request capacity.

See [learning notes](docs/learning-notes/README.md) for Siva's historical baseline results and instructions for recording your own.

## Contributing and branches

Published tasks live together on `main`; personal experiments belong on practice branches. See [task contribution and Git workflows](docs/contributing-tasks.md) for maintainer and learner workflows, including harder and fresh experiments.

## Future roadmap

Pool waiting and slow database work are the next exercise. Later topics may include transactional booking and overselling, idempotency, indexes and locks, caching, multiple instances, queues and retries, overload protection, observability, and failure recovery. These are learning goals, not implemented features or capacity guarantees.

The [architecture plan](docs/architecture-plan.md) describes future code organization. Only the learning documents are organized into task directories today.
