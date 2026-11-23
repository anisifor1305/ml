-- Задание 11: CROSS JOIN
-- Все сочетания cities и channels. Выведи city, channel. Порядок city ASC, channel ASC. До запуска предскажи число строк.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
SELECT c.city, ch.channel
FROM lesson10.cities AS c
CROSS JOIN lesson10.channels as ch
ORDER BY city ASC, channel ASC;