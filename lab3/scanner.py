import model

def input_dict(table_name, message, limit=1337):
    acceptable_keys = model.TABLES[table_name]

    print(message)
    print('(у форматі <attribute>=<value>)')
    print(f'Допустимі колонки: ({"/".join(acceptable_keys)})', end='\n\n')

    result = {}
    while limit > 0:
        data = input()
        if not data: break

        if data.count('=') != 1:
            print('Невдалий ввід')
            continue

        key, value = data.split('=')
        if key.lower() in [a_key.lower() for a_key in acceptable_keys]:
            result[key.strip()] = value.strip()
            limit = limit - 1
        else:
            print(f'Недопустина колонка `{key}` для таблиці `{table_name}`')

    return result


def input_simple(message):
    print(message, end='\n\n')

    return input()


def press_enter():
    print('\nНатисність ENTER щоб продовжити')
    input()