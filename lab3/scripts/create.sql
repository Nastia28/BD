CREATE TABLE master (
	id SERIAL NOT NULL, 
	name VARCHAR, 
	experience INTEGER, 
	rating FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE customer (
	id SERIAL NOT NULL, 
	name VARCHAR, 
	is_vip BOOLEAN, 
	PRIMARY KEY (id)
);

CREATE TABLE reservation (
	id SERIAL NOT NULL, 
	master_id INTEGER, 
	customer_id INTEGER, 
	datetime TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(master_id) REFERENCES master (id), 
	FOREIGN KEY(customer_id) REFERENCES customer (id)
);

CREATE TABLE procedure (
	id SERIAL NOT NULL, 
	reservation_id INTEGER, 
	price INTEGER, 
	work_type VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(reservation_id) REFERENCES reservation (id)
);

INSERT INTO master(name, experience, rating) VALUES
    ('Mary Jane', 15, 3.7),
    ('Jane Air', 3, 4.5),
    ('Violetta Blue', 8, 4.1),
    ('Crystal Maiden', 0, 1.5),
    ('Little Ann', 81, 4.99);

INSERT INTO customer(name, is_vip) VALUES
    ('William Red', false),
    ('Peter Snow', false),
    ('Johnny Good', false),
    ('Peter Rainy', true),
    ('Crusty Crab', true);

INSERT INTO reservation(master_id, customer_id, datetime) VALUES
    (1, 3, '2004-01-11T09:00:00'),
    (1, 4, '2005-02-12T10:00:00'),
    (2, 2, '2006-03-13T11:00:00'),
    (3, 1, '2007-04-14T12:00:00'),
    (4, 5, '2008-05-15T13:00:00'),
    (4, 1, '2009-06-16T14:00:00'),
    (5, 5, '2010-07-17T15:00:00'),
    (5, 1, '2011-08-18T16:00:00'),
    (5, 4, '2012-09-19T17:00:00');

INSERT INTO procedure(reservation_id, price, work_type) VALUES
    (1, 100, 'makeup cosmetic'),
    (2, 150, 'hair styling'),
    (3, 200, 'skin cryotherapy'),
    (4, 100, 'makeup cosmetic'),
    (5, 100, 'makeup cosmetic'),
    (6, 150, 'cutting nails'),
    (7, 300, 'eyebrow botox'),
    (8, 150, 'makeup cosmetic'),
    (9, 100, 'makeup cosmetic'),
    (1, 150, 'skin cryotherapy'),
    (2, 150, 'hair styling'),
    (3, 200, 'cutting nails'),
    (4, 100, 'makeup cosmetic');
