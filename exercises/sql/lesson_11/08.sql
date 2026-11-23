-- Задание 08: Витрина признаков
-- Выведи всех customers. Через WITH отдельно собери итоги и строку последнего заказа. last_amount — сумма последнего заказа, amount_change — последний минус предпоследний. Без заказов: orders_count = 0, остальные показатели NULL. С одним заказом: amount_change = NULL.
-- Столбцы: customer_id, name, orders_count, total_amount, last_amount, amount_change.
-- Сортировка: customer_id. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.
WITH prom as(
SELECT customer_id,
COUNT(*) AS orders_count,
SUM(amount) AS total_amount
FROM lesson10.orders
WHERE customer_id IS NOT NULL
GROUP BY customer_id
),
prom2 as (
    SELECT customer_id, order_id, amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id DESC) as rn,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_id ASC) as previous_amount
    FROM ORDERS
    WHERE customer_id IS NOT NULL
)
SELECT customers.customer_id, name,COALESCE(prom.orders_count, 0) AS orders_count, prom.total_amount, prom2.amount AS last_amount, prom2.amount - prom2.previous_amount AS amount_change
FROM customers
LEFT JOIN prom ON prom.customer_id=customers.customer_id
LEFT JOIN prom2 ON prom2.customer_id=customers.customer_id AND prom2.rn = 1