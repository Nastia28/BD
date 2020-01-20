ALTER TABLE master ADD COLUMN document tsvector;
UPDATE master SET document = to_tsvector(name) WHERE true;
CREATE INDEX gin_index ON master using gin(document);

DROP INDEX gin_index;

EXPLAIN SELECT * FROM master;
EXPLAIN SELECT * FROM master WHERE document @@ to_tsquery('foobar');