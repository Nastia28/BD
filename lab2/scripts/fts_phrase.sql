SELECT
    ts_headline(m.name, phraseto_tsquery('$PHRASE'), 'StartSel=[92m, StopSel=[0m'),
    ts_headline(c.name, phraseto_tsquery('$PHRASE'), 'StartSel=[92m, StopSel=[0m'),
    ts_headline(work_type, phraseto_tsquery('$PHRASE'), 'StartSel=[92m, StopSel=[0m')
FROM procedure
JOIN reservation ON procedure.reservation_id = reservation.id
JOIN master m on reservation.master_id = m.id
JOIN customer c on reservation.customer_id = c.id
WHERE to_tsvector(m.name) || to_tsvector(c.name) || to_tsvector(work_type) @@ phraseto_tsquery('$PHRASE');