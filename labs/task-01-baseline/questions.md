# Task 01 questions

Use your own recorded evidence. No answers or solution links are included. Keep the first baseline unchanged; implementation challenges belong on a separate practice branch.

## Easy

1. A sale page requests event 25. Which response fields would you inspect beyond the two automated checks?
2. Why can requested RPS and achieved RPS differ slightly even when no iterations are dropped?
3. What does P95 tell a booking engineer that the average alone does not?
4. Why is a 404 correct for event 10001 in the seed dataset but a problem for the current random-ID workload?
5. Measurement challenge: create your own learning note and record the same rate twice. What environment details make the comparison meaningful?

## Medium

1. At 300 requested RPS, achieved traffic is lower and dropped iterations appear. What evidence would distinguish a generator limitation from slow API responses?
2. All HTTP responses are 200, but some event-ID checks fail. Would you call the experiment successful? What evidence would you preserve?
3. Later runs have lower latency. Design an experiment to distinguish a run-order effect from an effect of increased traffic.
4. Implementation challenge, after the baseline: strengthen response checks for seeded event reads on your practice branch. How will you demonstrate that a deliberately incorrect response fails your checks?
5. Measurement challenge: design a repeatable CPU/memory sampling procedure. What could snapshots miss, and how would you report that limitation?

## Hard

1. Advanced experiment: design a comparison between uniform event reads and a sale dominated by one popular event. What must remain constant for the comparison to be useful?
2. A 60-second test passes at 300 RPS. What additional evidence would you require before promising a sustained ticket-sale traffic target?
3. Future components: booking writes and payments do not exist yet. Which correctness checks would be required before applying event-read capacity claims to those operations?
4. Advanced implementation challenge: design additional timing observations that distinguish connection acquisition from SQL execution without treating the current response-time header as either measurement. How would you account for instrumentation overhead?
5. CPU is below a presumed limit while requests become slower. Which waiting explanations would you investigate, and which require telemetry not currently available?
