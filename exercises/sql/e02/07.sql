-- E02, этап 6, задание 07: WITH и отбор итогов
-- Полное условие: docs/E02_ЭТАП_06_SQL.md
-- Таблицы: trips и zones; схемы lesson10 здесь НЕТ.
-- TODO: один SELECT (при необходимости с WITH) ниже.
WITH prom AS (
    SELECT pickup_zone_id,
    COUNT(*) AS trips_count,
    SUM(total) AS total_amount
    FROM trips
    WHERE pickup_zone_id IS NOT NULL
    GROUP BY pickup_zone_id
)

SELECT pickup_zone_id, trips_count, total_amount
FROM prom
WHERE trips_count >= 3
ORDER BY total_amount DESC, pickup_zone_id ASC
