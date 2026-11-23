-- Задание 02: Фильтр
-- Из customers выведи customer_id, name клиентов с age >= 30. Порядок customer_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT customer_id, name
FROM lesson10.customers
WHERE age>=30
ORDER BY customer_id ASC;