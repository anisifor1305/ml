-- E02, этап 6, задание 02: Две зоны: два LEFT JOIN
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
SELECT t.trip_id,
       p.zone AS pickup_zone,
       q.zone AS dropoff_zone
FROM trips AS t
LEFT JOIN zones AS p ON p.zone_id = t.pickup_zone_id
LEFT JOIN zones AS q ON q.zone_id = t.dropoff_zone_id
ORDER BY t.trip_id ASC;
