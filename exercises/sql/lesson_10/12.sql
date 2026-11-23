-- Задание 12: SELF JOIN
-- Через LEFT self-join staff выведи employee_id, имя сотрудника AS employee, имя руководителя AS manager. Сохрани сотрудника без руководителя. Порядок employee_id ASC.
-- Напиши один SELECT ниже. Все имена таблиц относятся к схеме lesson10.
-- TODO
select a.employee_id, a.name as employee, b.name AS manager
FROM lesson10.staff AS a
LEFT JOIN lesson10.staff AS b ON a.manager_id=b.employee_id
ORDER BY employee_id;