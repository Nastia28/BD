from consolemenu import SelectionMenu

import model
import view
import scanner


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.view = view.View()

        self.tables = list(model.TABLES.keys())

    def get_table_name(self, index):
        try:
            return self.tables[index]
        except IndexError:
            return None

    def show_start_menu(self, subtitle='', **kwargs):
        menu_options = self.tables + ['Створити 100 рандомних майстрів',
                                      'Зробити коміт']
        next_steps = [self.show_table_menu] * len(self.tables) + [
            self.create_random_masters,
            self.commit
        ]
        menu = SelectionMenu(menu_options, subtitle=subtitle,
                             title="Оберіть таблицю або дію:")
        menu.show()

        index = menu.selected_option
        if index < len(menu_options):
            table_name = self.get_table_name(index)
            next_step = next_steps[index]
            try:
                next_step(table_name=table_name)
            except Exception as err:
                self.show_start_menu(subtitle=str(err))
        else:
            print('Пока!!!!')

    def show_table_menu(self, table_name, subtitle=''):
        next_steps = [self.get, self.insert, self.update, self.delete, self.show_start_menu]
        menu = SelectionMenu(
            ['GET', 'INSERT', 'UPDATE', 'DELETE'], subtitle=subtitle,
            title=f'Обрано таблицю `{table_name}`', exit_option_text='Назад', )
        menu.show()

        next_step = next_steps[menu.selected_option]
        next_step(table_name=table_name)

    def get(self, table_name):
        filter_by = scanner.input_dict(table_name, 'За чим фільтрувати запит? Залиште пустим щоб отримати всі рядки:')
        data = self.model.get(table_name, **filter_by)
        self.view.print_entities(table_name, data)
        scanner.press_enter()
        self.show_table_menu(table_name)

    def insert(self, table_name):
        new_values = scanner.input_dict(table_name, 'Введіть нові значення:')
        self.model.insert(table_name, **new_values)
        self.show_table_menu(table_name, 'Вставка відбулася успішно')

    def update(self, table_name):
        filter_by = scanner.input_dict(table_name, 'Який рядок треба змінити?:', limit=1)
        new_values = scanner.input_dict(table_name, 'Введіть нові значення:')
        self.model.update(table_name, list(filter_by.items())[0], **new_values)
        self.show_table_menu(table_name, 'Оновлення відбулося успішно')

    def delete(self, table_name):
        filter_by = scanner.input_dict(table_name, 'Які рядки треба видалити?')
        self.model.delete(table_name, **filter_by)
        self.show_table_menu(table_name, 'Видалення відбулося успішно')

    def create_random_masters(self, **kwargs):
        self.model.create_random_masters()
        self.show_start_menu('100 випадкових майстрів додано')

    def commit(self, **kwargs):
        self.model.commit()
        self.show_start_menu(subtitle='Зміни успішно збережені')
