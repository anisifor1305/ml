-- E02, этап 6, задание 04: ROW_NUMBER внутри color
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
-- TODO: один SELECT (при необходимости с WITH) ниже.

SELECT trip_id, color,
ROW_NUMBER() OVER(PARTITION BY color
ORDER BY pickup_at ASC, trip_id ASC) AS rn
FROM trips
ORDER BY color ASC, pickup_at ASC, trip_id ASC;
