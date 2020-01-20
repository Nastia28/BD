INSERT INTO master (name, experience, rating)
SELECT
    md5(rand::text),
    (random() * 15)::integer,
    random() * 5
FROM generate_series(1, 100) as rand;
