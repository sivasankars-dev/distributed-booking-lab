# Distributed Booking Lab

Stage 1: one FastAPI process, PostgreSQL, 10,000 seeded events and a k6 baseline.
This is a learning starter, not a validated 5,000 RPS deployment. No booking,
Redis, queue, replicas or authentication have been implemented yet.

## Run on your Mac

Install and start Docker Desktop (with Compose v2). From this folder:

```bash
docker compose up --build -d
docker compose logs -f api
```

Press Ctrl+C to leave the log viewer; containers keep running.

```bash
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/ready
curl --fail http://localhost:8000/events/1
curl -i http://localhost:8000/events/10001
```

Expected: health `ok`, ready `ready`, event 1 with 1,000 available tickets,
and HTTP 404 for the last request. Swagger: http://localhost:8000/docs

## First experiment: 50 requests/sec for 30 seconds

```bash
docker compose --profile tools run --rm loadtest
```

The script exercises the real DB-backed endpoint, not the health endpoint.
Learning targets: P95 below 300 ms, errors below 1%, correct responses above
99%, and zero dropped iterations. A failed threshold gives a nonzero exit;
inspect the result instead of hiding the failure.

Increase traffic gradually:

```bash
RATE=100 DURATION=60s docker compose --profile tools run --rm loadtest
RATE=300 DURATION=60s docker compose --profile tools run --rm loadtest
docker stats
```

Requested RPS and achieved RPS can differ. Dropped iterations indicate k6
could not start all planned work; generator limits also need investigation.
API, DB and generator share your laptop, so this is not a production capacity
claim. Record results in docs/experiments.md before changing anything.

## Next experiment: change connection pool size

```bash
DB_POOL_SIZE=2 docker compose up -d --force-recreate api
RATE=300 DURATION=60s docker compose --profile tools run --rm loadtest
```

A small pool does not guarantee exhaustion with this fast query. Observe
rather than assuming a bottleneck. Restore the default with:

```bash
docker compose up -d --force-recreate api
```

## Stop and restart

```bash
docker compose down
docker compose up -d
```

The named volume retains data. init.sql runs only when that volume is first
initialized. Avoid deleting the volume unless intentionally resetting data.
The DB is not exposed to your host; the API binds only to localhost. Included
credentials are for this local lab only.

## Create a private GitHub repository

After extracting the starter, using GitHub CLI authenticated to your account:

```bash
git init -b main
git add .
git commit -m "Initialize FastAPI PostgreSQL learning lab"
gh repo create distributed-booking-lab --private --source=. --remote=origin --push
```

If the extracted folder already has Git metadata, skip git init and use its
existing repository. You can also create an empty private repository in the
GitHub website and follow its instructions to push an existing repository.

## Learning order

1. Measure this baseline and explain every component.
2. Add a second API replica and a load balancer.
3. Add Redis; compare cache hits and misses.
4. Implement booking with transactions and idempotency.
5. Add background jobs, retries and failure experiments.

Start by explaining why /health makes no DB call while /ready does, and why
one engine/pool is created per process rather than per request.
