-- Задание 02: Фильтр групп
-- Повтори итоги №01, оставь клиентов с двумя и более заказами через HAVING.
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
HAVING COUNT(*)>=2
ORDER BY customer_id;