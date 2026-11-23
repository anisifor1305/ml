-- Задание 08: LEFT JOIN и фильтр ON
-- Сохрани всех customers, добавив только orders со status paid. Условие status должно быть в ON. Те же четыре столбца и порядок, что в 07. Объясни, почему перенос status в WHERE теряет клиентов.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id=o.customer_id AND o.status='paid'
ORDER BY customer_id ASC, order_id ASC NULLS LAST;