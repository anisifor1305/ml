-- E02, этап 6, задание 06: Накопленная сумма
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
-- TODO: один SELECT (при необходимости с WITH) ниже.
SELECT trip_id, color, total,
SUM(total) OVER(PARTITION BY color ORDER BY pickup_at ASC, trip_id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM trips
ORDER BY color ASC, pickup_at ASC, trip_id ASC;
