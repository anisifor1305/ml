-- E02, этап 6, задание 08: Витрина признаков с историей до даты
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
-- TODO: один SELECT (при необходимости с WITH) ниже.
WITH prom AS (
    SELECT pickup_zone_id,
    COUNT(*) AS history_count,
    AVG(total) AS history_avg_total
    FROM trips
    WHERE( pickup_at<'2019-03-15 00:00:00') AND( dropoff_at<'2019-03-15 00:00:00') AND (dropoff_at >= pickup_at) AND (pickup_zone_id is not null)
    GROUP BY pickup_zone_id
)
SELECT trip_id, pickup_at, color, zones.zone AS pickup_zone, borough,
COALESCE(prom.history_count, 0) AS history_count, history_avg_total
FROM trips
LEFT JOIN zones on trips.pickup_zone_id=zones.zone_id
LEFT JOIN prom on trips.pickup_zone_id = prom.pickup_zone_id
WHERE pickup_at>='2019-03-15 00:00:00'
ORDER BY trip_id ASC
