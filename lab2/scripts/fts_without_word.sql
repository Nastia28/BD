SELECT m.name as master_name, c.name as customer_name, work_type
FROM procedure
JOIN reservation ON procedure.reservation_id = reservation.id
JOIN master m on reservation.master_id = m.id
JOIN customer c on reservation.customer_id = c.id
WHERE to_tsvector(m.name) || to_tsvector(c.name) || to_tsvector(work_type) @@ tsquery('!$WORD');