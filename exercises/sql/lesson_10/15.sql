-- Задание 15: Ловушка дубликатов
-- Соедини orders и tickets INNER JOIN по customer_id без фильтров статуса. Выведи order_id, ticket_id, amount. Порядок order_id ASC, ticket_id ASC. Не применяй DISTINCT. Объясни число строк и почему сумма amount по результату повторно учитывает заказы.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT o.order_id, t.ticket_id, o.amount
FROM orders as o
INNER JOIN tickets as t ON o.customer_id = t.customer_id
ORDER BY o.order_id ASC, t.ticket_id ASC
;