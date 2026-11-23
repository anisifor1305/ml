-- Задание 14: NULL-ловушка
-- Выведи customer_id, name клиентов, которых нет в blocklist. NULL в blocklist не обозначает конкретного клиента. Используй NOT EXISTS. Отдельно объясни, почему NOT IN с исходной blocklist даёт другой результат. Порядок customer_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT customer_id, name
FROM customers AS c
WHERE NOT EXISTS(
    SELECT 1
    FROM blocklist AS b
    WHERE b.customer_id = c.customer_id
)
ORDER BY customer_id ASC

;