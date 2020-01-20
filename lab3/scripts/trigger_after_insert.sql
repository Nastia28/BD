CREATE OR REPLACE FUNCTION after_insert_procedure()
RETURNS TRIGGER LANGUAGE PLPGSQL AS $$
DECLARE
    other_procedures CURSOR IS SELECT * FROM procedure WHERE reservation_id = NEW.reservation_id;
BEGIN
    FOR p IN other_procedures LOOP
        UPDATE procedure SET price = price * 0.9 WHERE id = p.id;
    END LOOP;
    RETURN NEW;
END;
$$;

DROP TRIGGER after_insert ON procedure;
CREATE TRIGGER after_insert AFTER INSERT ON procedure
    FOR EACH ROW EXECUTE PROCEDURE after_insert_procedure();

SELECT * from procedure WHERE reservation_id = 1;
INSERT INTO procedure(reservation_id, price, work_type)
VALUES (1, 100, 'something else');