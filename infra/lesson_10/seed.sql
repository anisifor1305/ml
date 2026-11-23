-- Только отдельная учебная схема; повторный запуск сохраняет существующие таблицы.
BEGIN;
CREATE SCHEMA IF NOT EXISTS lesson10;
SET LOCAL search_path TO lesson10;
CREATE TABLE IF NOT EXISTS customers (
    customer_id integer PRIMARY KEY,
    name text NOT NULL,
    city text,
    age integer CHECK (age >= 0)
);
CREATE TABLE IF NOT EXISTS orders (
    order_id integer PRIMARY KEY,
    customer_id integer REFERENCES customers(customer_id),
    amount numeric(10, 2) NOT NULL CHECK (amount >= 0),
    status text NOT NULL CHECK (status IN ('paid', 'cancelled', 'pending', 'refunded'))
);
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id integer PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES customers(customer_id),
    status text NOT NULL CHECK (status IN ('open', 'closed'))
);
CREATE TABLE IF NOT EXISTS staff (
    employee_id integer PRIMARY KEY,
    name text NOT NULL,
    manager_id integer REFERENCES staff(employee_id)
);
CREATE TABLE IF NOT EXISTS cities (city text PRIMARY KEY);
CREATE TABLE IF NOT EXISTS channels (channel text PRIMARY KEY);
-- NULL намеренно допустим: ловушка NOT IN.
CREATE TABLE IF NOT EXISTS blocklist (customer_id integer);
INSERT INTO customers VALUES
    (1, 'Ada', 'MSK', 30), (2, 'Boris', 'SPB', NULL),
    (3, 'Vera', 'MSK', 22), (4, 'Gleb', 'KZN', 40),
    (5, 'Dina', NULL, 27), (6, 'Egor', 'SPB', 35)
ON CONFLICT DO NOTHING;
INSERT INTO orders VALUES
    (101, 1, 100, 'paid'), (102, 1, 300, 'paid'),
    (103, 2, 200, 'cancelled'), (104, 3, 500, 'paid'),
    (105, NULL, 70, 'paid'), (106, 4, 120, 'pending'), (107, 1, 100, 'refunded')
ON CONFLICT DO NOTHING;
INSERT INTO tickets VALUES
    (501, 1, 'open'), (502, 1, 'closed'), (503, 2, 'open'), (504, 5, 'closed')
ON CONFLICT DO NOTHING;
INSERT INTO staff VALUES (1, 'Nina', NULL), (2, 'Oleg', 1), (3, 'Pavel', 1), (4, 'Rita', 2)
ON CONFLICT DO NOTHING;
INSERT INTO cities VALUES ('MSK'), ('SPB'), ('KZN') ON CONFLICT DO NOTHING;
INSERT INTO channels VALUES ('web'), ('app') ON CONFLICT DO NOTHING;
INSERT INTO blocklist SELECT 2 WHERE NOT EXISTS (SELECT 1 FROM blocklist);
INSERT INTO blocklist SELECT NULL WHERE NOT EXISTS (SELECT 1 FROM blocklist WHERE customer_id IS NULL);
COMMIT;
