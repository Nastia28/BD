from sqlalchemy import Column, Integer, String, DateTime, \
    Boolean, ForeignKey, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

db_str = 'postgres://postgres:gfhjkm@localhost:5432/salon'
db = create_engine(db_str, isolation_level='SERIALIZABLE')
Base = declarative_base()


class ReprMixin:
    def __repr__(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return f'<{self.__class__.__name__}>{clean_dict})'


class Master(Base, ReprMixin):
    __tablename__ = 'master'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    experience = Column(Integer)
    rating = Column(Float)

    reservation = relationship('Reservation')

    def __init__(self, id=None, name=None, experience=None, rating=None):
        self.id = id
        self.name = name
        self.experience = experience
        self.rating = rating


class Customer(Base, ReprMixin):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_vip = Column(Boolean)

    reservation = relationship('Reservation')

    def __init__(self, id=None, name=None, is_vip=None):
        self.id = id
        self.name = name
        self.is_vip = is_vip


class Reservation(Base, ReprMixin):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey('master.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    datetime = Column(DateTime)

    procedures = relationship('Procedure')

    def __init__(self, id=None, master_id=None, customer_id=None, datetime=None):
        self.id = id
        self.master_id = master_id
        self.customer_id = customer_id
        self.datetime = datetime


class Procedure(Base, ReprMixin):
    __tablename__ = 'procedure'

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'))
    price = Column(Integer)
    work_type = Column(String)

    def __init__(self, id=None, reservation_id=None, price=None, work_type=None):
        self.id = id
        self.reservation_id = reservation_id
        self.price = price
        self.work_type = work_type


Base.metadata.create_all(db)

TABLES = {
    'master': ('id', 'name', 'experience', 'rating'),
    'customer': ('id', 'name', 'is_vip'),
    'reservation': ('id', 'master_id', 'customer_id', 'datetime'),
    'procedure': ('id', 'reservation_id', 'price', 'work_type')
}

CLASSES = {
    'procedure': Procedure, 'customer': Customer,
    'reservation': Reservation, 'master': Master
}

COLUMN_TYPES = {
    'id': int, 'name': str, 'experience': int, 'rating': float, 'is_vip': bool,
    'master_id': int, 'customer_id': int, 'datetime': str
}


def prepare_values_dict(dictionary):
    for key, value in dictionary.items():
        constructor = COLUMN_TYPES[key]
        dictionary[key] = constructor(value)


class Model:
    def __init__(self):
        self.session = sessionmaker(db)()

    def create_tables(self):
        with open('scripts/create.sql') as file:
            command = file.read()
            self.session.execute(command)
            self.session.commit()

    def get(self, table_name, **filter_by):
        objects_class = CLASSES[table_name]
        objects = self.session.query(objects_class)
        for key, item in filter_by.items():
            objects = objects.filter(getattr(objects_class, key) == item)

        return list(objects)

    def insert(self, table_name, **new_values):
        prepare_values_dict(new_values)
        object_class = CLASSES[table_name]
        obj = object_class(**new_values)
        self.session.add(obj)

    def update(self, table_name, condition, **new_values):
        if not new_values:
            raise Exception('Не вказані поля, які треба оновити')

        prepare_values_dict(new_values)
        column, value = condition
        object_class = CLASSES[table_name]
        filter_attr = getattr(object_class, column)
        objects = self.session.query(object_class).filter(filter_attr == value)

        for obj in objects:
            for key, item in new_values.items():
                setattr(obj, key, item)

    def delete(self, table_name, **filter_by):
        if not filter_by:
            raise Exception('Не вказані умови для рядків, які треба видалити')

        objects_class = CLASSES[table_name]
        objects = self.session.query(objects_class)
        for key, item in filter_by.items():
            objects = objects.filter(getattr(objects_class, key) == item)

        objects.delete()

    def commit(self):
        self.session.commit()

    def create_random_masters(self):
        with open('scripts/random.sql') as file:
            sql = file.read()
            self.session.execute(sql)
