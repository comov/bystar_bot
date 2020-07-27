users = [
    {
        'email': 'john_1_doe_1@example.com',
        'first_name': '',
        'last_name': '',
    },
    {
        'email': 'john_2_doe_2@example.com',
        'first_name': '',
        'last_name': 'Doe_2',
    },
    {
        'email': 'john_3_doe_3@example.com',
        'first_name': 'John_3',
        'last_name': '',
    },
    {
        'email': 'john_4_doe_4@example.com',
        'first_name': 'John_4',
        'last_name': 'Doe_4',
    },
]

def print_hello_messages(user: dict):
    name = user['email']
    # TODO: тут нужен код который создает имя пользователя и присваивает его переменной "name"
    if user['first_name'] and user['last_name']:
        name = user['first_name'] + ' ' + user['last_name']

    if user['first_name'] and not user['last_name']:
        name = user['first_name']

    if user['last_name'] and not user['first_name']:
        name = user['last_name']

    print(f'Привет {name}! Рад тебя приветствовать!')


if __name__ == '__main__':
    for user_dict in users:  # type: dict
        print_hello_messages(user_dict)
