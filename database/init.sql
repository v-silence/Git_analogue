CREATE TABLE IF NOT EXISTS commits (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,
    message TEXT NOT NULL,
    creator TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL
);


INSERT INTO users (username, password) VALUES ('user1', '111');
INSERT INTO users (username, password) VALUES ('user2', '222');