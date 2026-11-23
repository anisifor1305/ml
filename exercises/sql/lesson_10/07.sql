-- Задание 07: LEFT JOIN
-- Сохрани всех customers и добавь их orders. Выведи customer_id из customers, name, order_id, amount. Порядок customer_id ASC, order_id ASC NULLS LAST. Не заполняй NULL нулями.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id=o.customer_id
ORDER BY customer_id ASC, order_id ASC NULLS LAST;