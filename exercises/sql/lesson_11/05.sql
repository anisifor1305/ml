-- Задание 05: Накопление и скользящее среднее
-- В порядке order_id внутри клиента посчитай сумму от первого заказа до текущего и среднее по текущему и предыдущему заказам. Используй явные рамки ROWS.
-- Столбцы: order_id, customer_id, amount, running_total, moving_avg.
-- Сортировка: customer_id, order_id. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.

SELECT order_id, customer_id, amount,
SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
AVG(amount) OVER (PARTITION BY customer_id ORDER BY order_id
    ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS moving_avg
FROM lesson10.orders
WHERE customer_id IS NOT NULL
ORDER BY customer_id, order_id;