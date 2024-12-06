CREATE TABLE IF NOT EXISTS commits (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);
