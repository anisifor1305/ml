-- E02, этап 6, задание 01: Зона отправления: LEFT JOIN
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
-- TODO: один SELECT (при необходимости с WITH) ниже.
SELECT trip_id, color, total,
zones.zone AS pickup_zone
, borough
FROM trips
LEFT JOIN zones on trips.pickup_zone_id=zones.zone_id
ORDER BY trip_id ASC;
