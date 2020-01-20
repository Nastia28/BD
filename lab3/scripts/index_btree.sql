CREATE INDEX btree_index ON master using btree(id);
DROP INDEX btree_index;

EXPLAIN SELECT * FROM master;
EXPLAIN SELECT * FROM master WHERE id = 10000;