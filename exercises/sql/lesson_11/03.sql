-- Задание 03: Итог рядом с заказом
-- Добавь к каждой строке заказа общую сумму заказов его клиента через окно.
-- Столбцы: order_id, customer_id, amount, customer_total.
-- Сортировка: customer_id, order_id. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.

SELECT order_id, customer_id, amount,
SUM(amount) OVER (PARTITION BY customer_id) AS customer_total
FROM lesson10.orders
WHERE customer_id IS NOT NULL
ORDER BY customer_id, order_id;