-- Задание 09: RIGHT JOIN
-- Напиши customers RIGHT JOIN orders, сохрани все заказы, включая анонимный. Выведи order_id, customer_id из customers, name, amount. Порядок order_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT o.order_id, c.customer_id, c.name, o.amount
FROM customers AS c
RIGHT JOIN orders AS o ON c.customer_id=o.customer_id
ORDER BY order_id ASC;