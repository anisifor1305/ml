-- Задание 05: Подзапрос IN
-- Из orders выведи order_id, customer_id, amount заказов клиентов из MSK. Используй IN с подзапросом к customers. Порядок order_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT order_id, customer_id, amount
FROM orders
WHERE customer_id IN (
    SELECT customer_id
    FROM customers
    WHERE city='MSK'
)
ORDER BY order_id ASC;