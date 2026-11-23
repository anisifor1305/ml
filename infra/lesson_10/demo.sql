-- Отдельные маленькие таблицы только для примеров лекции; не данные заданий.
BEGIN;
CREATE SCHEMA IF NOT EXISTS lesson10_demo;
SET LOCAL search_path TO lesson10_demo;
CREATE TABLE IF NOT EXISTS teams (team_id integer PRIMARY KEY, title text NOT NULL);
CREATE TABLE IF NOT EXISTS people (
    person_id integer PRIMARY KEY, name text NOT NULL, age integer,
    team_id integer REFERENCES teams(team_id), manager_id integer REFERENCES people(person_id)
);
CREATE TABLE IF NOT EXISTS payments (
    payment_id integer PRIMARY KEY, person_id integer REFERENCES people(person_id),
    amount numeric(10, 2)
);
INSERT INTO teams VALUES (1, 'Research'), (2, 'Platform'), (3, 'Vision') ON CONFLICT DO NOTHING;
INSERT INTO people VALUES
    (10, 'Alina', 28, 1, NULL), (20, 'Max', NULL, 2, 10), (30, 'Olya', 35, NULL, 10)
ON CONFLICT DO NOTHING;
INSERT INTO payments VALUES (201, 10, 100), (202, 10, 300), (203, 20, NULL), (204, NULL, 50)
ON CONFLICT DO NOTHING;
COMMIT;
