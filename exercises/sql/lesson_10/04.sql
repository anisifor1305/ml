-- Задание 04: Сортировка и LIMIT
-- Из orders выведи order_id, amount трёх самых дорогих заказов независимо от status. Сортировка amount DESC, затем order_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT order_id, amount
FROM orders
ORDER BY amount DESC, order_id ASC
LIMIT 3;