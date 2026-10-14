# Distributed Booking Lab

Learn distributed systems by building, changing, testing, and debugging a booking application.

This repository is for beginners who want to understand how backend systems work in practice.

We start with a small application. Each task introduces a concept, gives you something to implement, and helps you investigate real production problems.

## Our purpose

The goal is to make distributed systems easier to learn through hands-on work.

You will:

- Learn concepts in simple English.
- Read and understand working code.
- Make changes in your local copy.
- Generate traffic and introduce controlled failures.
- Observe system behaviour.
- Investigate problems and test your ideas.
- Record what you learned.

The tasks focus on booking systems and real production situations. Interview preparation is a possible benefit, but it is not the purpose of this project.

## Who can use this repository?

You do not need previous distributed systems experience.

Basic knowledge of Python, APIs, SQL, and terminal commands will help. Concept documents will explain the distributed systems terms used in each task.

Start with the beginner tasks and move forward at your own pace.

## How learning works

Each task will have three separate documents.

| Document | Purpose |
| --- | --- |
| Concept | Explains the topic, technical terms, and relevant code |
| Task | Gives the implementation steps, experiments, checks, and reset instructions |
| Questions | Contains follow-up challenges and production problem questions |

If a task feels confusing, open its concept document, learn the topic, and return to the task.

### Your learning flow

1. Read the task and its learning goals.
2. Open the concept document when you need an explanation.
3. Predict what will happen.
4. Implement the change in your local repository.
5. Run the experiment.
6. Collect evidence and check correctness.
7. Work through the follow-up questions.
8. Record your findings.

The question documents will not contain answers or solution links.

Research the questions using documentation, experiments, and other reliable sources. Where a question asks for an implementation, change the code and test your approach.

## Question difficulty

Each task's questions will be grouped by difficulty.

| Level | Focus |
| --- | --- |
| Easy | Explain the concept, inspect the code, and make a small change |
| Medium | Compare approaches, implement an improvement, and investigate a failure |
| Hard | Handle interacting failures, protect correctness, and evaluate production trade-offs |

Difficulty describes the work involved. It does not mean that every question has one correct answer.

Use evidence to support your explanation.

## Task documentation standards

Every task will explain:

- What you will learn
- Required knowledge and previous tasks
- The related concept document
- Which files you may change
- Which shared interfaces must remain compatible
- What to implement
- How to run the experiment
- What to measure
- How to check correctness
- How to stop or reset the experiment
- Where to find its follow-up questions

Technical terms will be explained in the concept document and linked where needed.

A task will distinguish expected behaviour from results that depend on your machine or workload.

## Independent tasks and reusable code

Experiments should be safe to change without breaking other tasks.

We will follow these rules:

1. Keep task-specific behaviour inside that task's module.
2. Keep reusable code in clearly separated shared modules.
3. Use task-specific configuration for experimental behaviour.
4. Avoid changing shared defaults to reproduce a task's failure.
5. Keep shared interfaces compatible with existing tasks.
6. Keep experimental delays and failures disabled by default.
7. Use separate data or a documented reset process where tasks modify state.
8. Run relevant compatibility checks when shared code changes.

Reusable code may include database connection handling, configuration, logging, and other behaviour needed by multiple tasks.

Tasks may intentionally build on earlier tasks. Those dependencies will be documented.

Isolation does not mean copying all shared code into every task. It means that a task's implementation and experiments should not unexpectedly change another task's behaviour.

### Working on your own changes

Use a separate Git branch for each task:

```bash
git switch -c task/connection-pool
```

A branch keeps your work separate from the baseline. Module boundaries, configuration, and data isolation protect behaviour while the system runs.

Commit your progress so you can compare changes and return to a known state.

## Current status

**Stage 1 starter code is available.**

It includes:

- One FastAPI process
- One PostgreSQL database
- 10,000 sample events
- An endpoint to read event details
- Health and database readiness checks
- A configurable database connection pool
- A k6 load-test script
- An experiment record template

Booking, caching, queues, multiple API instances, and controlled failure scenarios are not implemented yet.

The separate concept, task, and question documents described above are planned. The current code has not yet been reorganized into isolated task modules.

## Run the current starter

### Requirements

- Git
- Docker Desktop with Docker Compose
- Docker Desktop running

The commands below use macOS/Linux shell syntax.

### Clone the repository

```bash
git clone https://github.com/sivasankars-dev/distributed-booking-lab.git
cd distributed-booking-lab
```

If you already have the project, open a terminal in its folder.

### Start the application

```bash
docker compose up --build -d
docker compose ps
```

View API logs:

```bash
docker compose logs -f api
```

Press Ctrl+C to leave the log viewer. The containers will keep running.

### Check the endpoints

```bash
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/ready
curl --fail http://localhost:8000/events/1
curl -i http://localhost:8000/events/10001
```

| Endpoint | Expected result |
| --- | --- |
| `/health` | HTTP 200: the API can respond |
| `/ready` | HTTP 200 when the database check succeeds |
| `/events/1` | Event details with 1,000 available tickets |
| `/events/10001` | HTTP 404: the event does not exist |

Interactive API documentation:

http://localhost:8000/docs

## Local configuration

The current starter works without a `.env` file because configuration defaults are already provided.

A documented `.env.example` is planned. Once available, you will be able to copy it:

```bash
cp .env.example .env
```

Each setting will explain its purpose, default value, and effect.

The example file will be committed. Your local `.env` file will remain excluded from Git.

## Current code structure

| Path | Purpose |
| --- | --- |
| `app/main.py` | API endpoints and database connection pool |
| `db/init.sql` | Events table and sample data |
| `compose.yaml` | API, database, and load-test container configuration |
| `Dockerfile` | API container build |
| `requirements.txt` | Python dependencies |
| `loadtests/baseline.js` | Baseline traffic generator |
| `docs/experiments.md` | Experiment record template |

## Planned learning structure

| Path | Purpose |
| --- | --- |
| `docs/start-here.md` | Basics and instructions for using the lab |
| `docs/concepts/` | Simple explanations of each topic |
| `docs/tasks/` | Implementation and experiment instructions |
| `docs/questions/` | Easy, medium, and hard questions without answers |
| `docs/glossary.md` | Definitions of technical terms |
| `docs/learning-notes/` | My experiments, findings, and corrections |
| `app/core/` | Shared application code |
| `app/tasks/` | Task-specific application code |
| `loadtests/tasks/` | Task-specific load tests |

This structure is proposed. It will be introduced gradually as tasks are implemented.

## First baseline experiment

A baseline is the starting measurement used to compare later changes.

Run:

```bash
docker compose --profile tools run --rm loadtest
```

The script schedules 50 event requests per second for 30 seconds.

Increase traffic gradually:

```bash
RATE=100 DURATION=60s docker compose --profile tools run --rm loadtest
RATE=300 DURATION=60s docker compose --profile tools run --rm loadtest
```

Watch resource usage in another terminal:

```bash
docker stats
```

### Measurements

| Metric | Meaning |
| --- | --- |
| Achieved RPS | Requests actually executed per second |
| P95 latency | 95% of requests took this long or less |
| Error rate | Percentage of failed requests |
| Checks | Whether responses passed the script's checks |
| Dropped iterations | Planned work the load generator could not start |

The starter's practice targets are:

- P95 below 300 ms
- Request failures below 1%
- More than 99% of checks passing
- Zero dropped iterations

These are exercise targets, not measured results or universal production requirements.

A failed target is something to investigate. It does not automatically identify which component caused the problem.

## Planned production topics

The booking application will provide practical situations for learning these topics.

| Area | Example topics and problems |
| --- | --- |
| Traffic and capacity | Workload estimation, RPS, QPS, saturation, load testing |
| Database performance | Slow queries, indexes, connection pools, lock contention |
| Booking correctness | Concurrent reservations, overselling, transactions, idempotency |
| Caching | Cache misses, stale availability, invalidation, cache stampedes |
| Multiple instances | Load balancing, stateless APIs, health checks, instance failure |
| Background processing | Queue backlogs, retries, redelivery, duplicate processing |
| Service communication | Downstream delays, timeouts, cancellation, retry storms |
| Overload protection | Rate limiting, backpressure, bounded queues |
| Distributed workflows | Reservation expiry, partial failure, compensation, outbox |
| Data distribution | Replication, stale reads, partitioning, hot keys |
| Observability | Logs, metrics, traces, incident investigation |
| Deployment and recovery | Graceful shutdown, rolling changes, recovery checks |

These topics form an evolving roadmap. Each available task will have its own status and prerequisites.

## Scale goals

We want to explore workloads associated with millions of daily active users and peak traffic around 5,000 requests per second.

These are learning goals, not verified system capacity.

Daily active users, API requests per second, and database queries per second measure different things.

For every capacity result, record the workload, hardware, configuration, and test duration.

The API, database, and load generator initially share your computer. They compete for resources. Later experiments may use separate machines.

## My learning and teaching progress

I will publish learning notes as I complete experiments.

Each note will include:

- My original question and prediction
- What I implemented
- The environment and configuration
- Results and supporting evidence
- Mistakes or incorrect assumptions
- What changed in my understanding
- Remaining questions

Task statuses will mean:

| Status | Meaning |
| --- | --- |
| Planned | Not ready to use |
| Ready to try | Code and learning documents are available |
| Verified | The experiment was run in a documented environment |

Verification does not guarantee identical performance on every machine.

## Record your own learning

For each experiment, record:

1. Question and prediction
2. Git commit and configuration
3. Traffic and dataset
4. Correctness checks
5. Latency, errors, and resource usage
6. Change made
7. Before-and-after results
8. Explanation and trade-offs
9. Questions still unanswered

Do not judge a fix only by speed. A faster system that creates duplicate bookings or loses work is not a successful fix.

## Stop and restart

```bash
docker compose down
docker compose up -d
```

The database volume retains your data.

`db/init.sql` runs only when PostgreSQL initializes an empty data volume. Editing it does not update an existing database automatically.

Future tasks will provide their own reset instructions.

## Troubleshooting

| Problem | First check |
| --- | --- |
| Docker daemon unavailable | Start Docker Desktop |
| Port 8000 already used | Stop the application using that port |
| API unavailable | Inspect `docker compose ps` and API logs |
| Database startup failure | Inspect `docker compose logs db` |
| Readiness returns HTTP 503 | Inspect API and database logs |
| Load-test targets fail | Inspect latency, failures, and dropped iterations |

The included credentials are for local learning. The API binds to localhost, and the database is not exposed on a host port.

## Learning principle

Understand the concept. Make a change. Run the experiment. Investigate the evidence. Explain what you learned.

Progress comes from understanding behaviour and protecting correctness, not from adding more tools.