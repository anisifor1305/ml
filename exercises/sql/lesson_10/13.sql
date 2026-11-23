-- Задание 13: EXISTS
-- Выведи customer_id, name клиентов, у которых есть хотя бы один открытый ticket (status open). Используй коррелированный EXISTS; каждый клиент ровно один раз. Порядок customer_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT customer_id, name
FROM customers AS c
WHERE EXISTS(
    SELECT 1
    FROM tickets as T
    WHERE status='open'
    AND t.customer_id = c.customer_id
)
ORDER BY customer_id ASC

;