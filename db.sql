GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO repl_user;
ALTER USER repl_user WITH SUPERUSER;

CREATE SCHEMA raw;

CREATE TABLE public.orders (
    user_id SERIAL PRIMARY KEY,
    order_id UUID NOT NULL UNIQUE,
    event_key VARCHAR,
    product_name VARCHAR,
    description VARCHAR,
    price DOUBLE PRECISION,
    event_timestamp TIMESTAMP,
    operation VARCHAR
);

CREATE TABLE public.transactions (
    transaction_id VARCHAR PRIMARY KEY,
    transaction JSONB
);

CREATE TABLE raw.orders (
    user_id SERIAL PRIMARY KEY,
    order_id UUID NOT NULL UNIQUE,
    event_key VARCHAR,
    product_name VARCHAR,
    description VARCHAR,
    price DOUBLE PRECISION,
    event_timestamp TIMESTAMP,
    operation VARCHAR
);
