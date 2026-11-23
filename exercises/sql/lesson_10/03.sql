-- Задание 03: Пропуски
-- Выведи customer_id, name клиентов с неизвестным возрастом. Порядок customer_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT customer_id, name
FROM lesson10.customers
WHERE age is NULL
ORDER BY customer_id ASC;