CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    amount NUMERIC(10,2) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    user_id INT,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    performed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    details JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE users_backup (
    LIKE users INCLUDING ALL
);
