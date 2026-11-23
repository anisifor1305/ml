-- Задание 01: Итоги по клиентам
-- Посчитай число заказов и сумму по каждому клиенту с заказами.
-- Столбцы: customer_id, orders_count, total_amount.
-- Сортировка: customer_id. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.
SELECT c.customer_id,
COUNT(*) AS orders_count ,SUM(amount) AS total_amount
FROM lesson10.customers AS c
JOIN lesson10.orders AS o ON c.customer_id=o.customer_id
GROUP BY c.customer_id
ORDER BY customer_id;