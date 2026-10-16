# Task 02 questions

**Planned — requires application implementation before running.** Reasoning questions can be explored now. Implementation challenges refer to future work and do not assume timing telemetry already exists. There are no answers, worked solutions, or solution links here.

## Easy

1. A booking request owns a connection while PostgreSQL sleeps. What resource remains occupied even if CPU is low?
2. How is waiting to obtain a connection different from waiting for an already-running query?
3. Which assumptions are needed for the estimate `5 / 0.1 ≈ 50`? Which would you measure first?
4. Future implementation challenge: validate task-specific settings and demonstrate that invalid enabled settings are rejected. How will you check disabled mode?
5. Why should the initial experiment use a dedicated pool and leave the baseline script unchanged?

## Medium

1. After future instrumentation exists, acquisition duration rises while query duration stays similar. What additional evidence would you gather before explaining the cause?
2. At 100 requested RPS, many responses fail quickly. How could total achieved RPS hide low successful-work throughput?
3. Future implementation challenge: distinguish pool timeout, statement timeout, and client timeout in results. What checks would expose a misleading error classification?
4. A slow availability check times out and the caller retries immediately. How might retries change offered load during a sale? Design a controlled comparison without assuming retries improve success.
5. Future implementation challenge: verify connections are released after request cancellation and query failure. What evidence would reveal a leak across repeated runs?
6. Why might increasing pool size reduce waiting in one experiment but worsen database behaviour in another?

## Hard

1. Advanced / future multiple-process deployment: each API process owns a task pool and a baseline pool. How would you budget connections across replicas and PostgreSQL limits?
2. Advanced implementation challenge: propose overload protection for a sudden sale spike. How would you evaluate bounded waiting, rejection, and fairness between ordinary browsing and booking traffic?
3. Future booking writes: a client times out after a reservation might have committed. What correctness risks would automatic retries introduce, and what additional components would be needed?
4. Advanced measurement challenge: design observations that separate cold connection creation, pool contention, and query execution without leaking credentials or creating excessive telemetry overhead.
5. Advanced interference experiment: how would you deliberately study shared PostgreSQL contention between two separate pools while preserving a meaningful sequential control run?
6. Advanced implementation challenge: design graceful shutdown under load. What happens to queued, executing, and cancelled requests, and how would you prove cleanup without losing evidence?
