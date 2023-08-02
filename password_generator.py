import random
import string


def characters_check(letters_list):
    length = 12
    selected_few = random.choices(letters_list, k=length)
    random.shuffle(selected_few)

    return "".join(selected_few)


def numbers_check(numbers_list):
    length = 5
    numbers_select = random.choices(numbers_list, k=length)
    random.shuffle(numbers_select)
    return int("".join(map(str, numbers_select)))


def symbols_check(symbols_list):
    length = 3
    symbols = random.choices(symbols_list, k=length)
    return symbols


def password_output(letters, numbers, symbols):
    password = list(letters) + list(str(numbers)) + list(symbols)
    random.shuffle(password)
    return "".join(password)


def generate_password():
    characters = list(string.ascii_letters)
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    symbols = ["!", "@", "?", "&", "£", "#", "_", "-", "*", "%", "$", "/", "(", ")", "="]

    return password_output(characters_check(characters), numbers_check(numbers), symbols_check(symbols))