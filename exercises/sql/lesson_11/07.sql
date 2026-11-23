-- Задание 07: Топ-2 на клиента
-- Через WITH и ROW_NUMBER оставь до двух самых дорогих заказов на клиента. При равной сумме меньший order_id идёт первым.
-- Столбцы: customer_id, order_id, amount.
-- Сортировка: customer_id ASC, amount DESC, order_id ASC. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.

WITH prom as (
SELECT customer_id, order_id, amount,
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY customer_id, amount DESC, order_id) as r_n
FROM lesson10.orders
)
SELECT customer_id, order_id, amount
FROM prom
WHERE r_n <= 2 AND customer_id IS NOT NULL;