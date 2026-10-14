CREATE TABLE events (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    total_tickets INTEGER NOT NULL CHECK (total_tickets >= 0),
    available_tickets INTEGER NOT NULL CHECK (available_tickets BETWEEN 0 AND total_tickets)
);
INSERT INTO events (id, name, total_tickets, available_tickets)
SELECT n, 'Learning Event ' || n, 1000, 1000
FROM generate_series(1, 10000) AS n;
