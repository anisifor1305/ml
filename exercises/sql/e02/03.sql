-- E02, этап 6, задание 03: Все зоны и их итоги
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
-- TODO: один SELECT (при необходимости с WITH) ниже.
SELECT zone_id, zone,
count(trips.trip_id) AS trips_count,
SUM(trips.total) AS total_amount
FROM zones
LEFT JOIN trips ON zones.zone_id=trips.pickup_zone_id
GROUP BY zones.zone_id, zones.zone
ORDER BY zone_id ASC;
