-- Задание 04: Предыдущий заказ
-- Найди предыдущую сумму через LAG в порядке order_id внутри клиента. amount_change — текущая минус предыдущая сумма. Для первого заказа оба поля NULL.
-- Столбцы: order_id, customer_id, amount, previous_amount, amount_change.
-- Сортировка: customer_id, order_id. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.
SELECT order_id, customer_id, amount,
LAG(amount) OVER (PARTITION BY customer_id) as previous_amount,
amount-LAG(amount) OVER (PARTITION BY customer_id) as amount_change
from lesson10.orders
WHERE customer_id IS NOT NULL
ORDER BY customer_id, order_id;