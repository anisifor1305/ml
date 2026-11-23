-- Задание 06: INNER JOIN
-- Соедини customers и orders. Выведи customer_id из customers, name, order_id, amount только совпавших пар. Порядок order_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers AS c
INNER JOIN orders AS o ON c.customer_id=o.customer_id;