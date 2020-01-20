class View:
    def __init__(self):
        self.SEPARATOR_WIDTH = 30

    def print_entities(self, table_name, data):
        entities, cols = data
        separator_line = '-' * self.SEPARATOR_WIDTH

        print(f'Результат для таблиці `{table_name}`', end='\n\n')
        print(separator_line)
        print('|'.join(cols))
        print(separator_line)
        for entity in entities:
            print('|'.join([str(col) for col in entity]))
