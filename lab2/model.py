import psycopg2

TABLES = {
    'master': ('id', 'name', 'experience', 'rating'),
    'customer': ('id', 'name', 'is_vip'),
    'reservation': ('id', 'master_id', 'customer_id', 'datetime'),
    'procedure': ('id', 'reservation_id', 'price', 'work_type')
}


class Model:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='salon' user='postgres'"
                                     "host='localhost' password='gfhjkm'")
        self.cursor = self.conn.cursor()

    def create_tables(self):
        with open('scripts/create.sql') as file:
            command = file.read()
            self.cursor.execute(command)
            self.conn.commit()

    def get(self, table_name, **filter_by):
        command = f'SELECT * FROM {table_name}'

        if filter_by:
            conditions = [f"{column}='{filter_by[column]}'" for column in filter_by]
            command = f'{command} where {" and ".join(conditions)}'

        self.cursor.execute(command)
        return self.cursor.fetchall(), TABLES[table_name]

    def insert(self, table_name, **new_values):
        if not new_values:
            raise Exception('Не вказані поля, які треба заповнити')

        try:
            columns = new_values.keys()
            values = [f"'{value}'" for value in new_values.values()]
            command = f'INSERT INTO {table_name} ({", ".join(columns)})' + \
                      f'VALUES ({", ".join(values)})'

            self.cursor.execute(command)
        finally:
            self.conn.commit()

    def update(self, table_name, condition, **new_values):
        if not new_values:
            raise Exception('Не вказані поля, які треба оновити')

        try:
            column, value = condition
            updates = ', '.join([f"{column} = '{new_values[column]}'" for column in new_values])
            command = f'UPDATE {table_name} SET {updates} WHERE {column}={value}'

            self.cursor.execute(command)
        finally:
            self.conn.commit()

    def delete(self, table_name, **filter_by):
        if not filter_by:
            raise Exception('Не вказані умови для рядків, які треба видалити')

        try:
            conditions = [f"{column}='{filter_by[column]}'" for column in filter_by]
            command = f'DELETE FROM {table_name} WHERE {" and ".join(conditions)}'

            self.cursor.execute(command)
        finally:
            self.conn.commit()

    def get_masters_by_procedures(self, procedures):
        procedures = [f"'{p.lower()}'" for p in procedures]
        command = f'''
        SELECT name FROM master
        JOIN reservation r on master.id = r.master_id
        JOIN procedure p on p.reservation_id = r.id
        WHERE lower(work_type) in ({", ".join(procedures)})
        GROUP BY name;'''

        self.cursor.execute(command)
        return self.cursor.fetchall(), ('name',)

    def get_procedure_by_client_type(self, is_vip):
        command = f'''
        SELECT work_type FROM procedure
        JOIN reservation r on "procedure".reservation_id = r.id
        JOIN customer c2 on r.customer_id = c2.id
        WHERE c2.is_vip={is_vip}
        GROUP BY work_type;'''

        self.cursor.execute(command)
        return self.cursor.fetchall(), ('work_type',)

    def fts_without_word(self, word):
        with open('scripts/fts_without_word.sql') as file:
            sql = file.read().replace('$WORD', word)
            self.cursor.execute(sql)
            return self.cursor.fetchall(), ('master_name', 'customer_name', 'work_type')

    def fts_phrase(self, phrase):
        with open('scripts/fts_phrase.sql') as file:
            sql = file.read().replace('$PHRASE', phrase)
            self.cursor.execute(sql)
            return self.cursor.fetchall(), ('master_name', 'customer_name', 'work_type')

    def create_random_masters(self):
        try:
            with open('scripts/random.sql') as file:
                sql = file.read()
                self.cursor.execute(sql)
        finally:
            self.conn.commit()
