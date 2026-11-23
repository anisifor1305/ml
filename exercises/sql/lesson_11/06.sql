-- Задание 06: Ранги
-- Посчитай ROW_NUMBER, RANK и DENSE_RANK по amount DESC внутри клиента. Только для ROW_NUMBER разреши равенство через order_id ASC. Сравни номера заказов с равной суммой.
-- Столбцы: order_id, customer_id, amount, row_num, rank_num, dense_rank_num.
-- Сортировка: customer_id ASC, amount DESC, order_id ASC. Если направление не указано, ASC.
-- Таблицы: lesson10.orders и lesson10.customers. Все статусы учитываются.
-- Заказы без customer_id исключи. order_id задаёт учебную хронологию.
-- TODO: напиши один запрос.

SELECT order_id, customer_id, amount,
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC, order_id ) as row_num,
RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) as rank_num,
DENSE_RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) as dense_rank_num
FROM lesson10.orders
WHERE customer_id IS NOT NULL
ORDER BY customer_id, amount DESC, order_id;