CREATE OR REPLACE FUNCTION after_update_reservation()
RETURNS TRIGGER LANGUAGE PLPGSQL AS $$
DECLARE
BEGIN
    IF true IN (SELECT is_vip FROM customer WHERE id = NEW.customer_id) THEN
        UPDATE master SET rating = rating * 1.1 WHERE id = NEW.master_id;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER after_update ON reservation;
CREATE TRIGGER after_update AFTER UPDATE ON reservation
    FOR EACH ROW EXECUTE PROCEDURE after_update_reservation();

INSERT INTO master(id, name, experience, rating) VALUES (1337, 'Sample Master', 15, 4);
INSERT INTO customer(id, name, is_vip) VALUES (42, 'Simple Customer', false);
INSERT INTO customer(id, name, is_vip) VALUES (1337, 'Vip Customer', true);
INSERT INTO reservation(master_id, customer_id) VALUES (1337, 42);
UPDATE reservation SET customer_id = 1337 WHERE master_id = 1337;
SELECT * FROM master WHERE name = 'Sample Master';