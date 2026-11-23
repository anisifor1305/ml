-- Задание 10: FULL JOIN
-- Полное соединение customers и orders. Выведи customer_id из customers, name, order_id, amount. Порядок customer_id ASC NULLS LAST, order_id ASC NULLS LAST. Объясни число строк.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers AS c
FULL JOIN orders AS o ON c.customer_id=o.customer_id
ORDER BY customer_id ASC NULLS LAST, order_id ASC NULLS LAST;