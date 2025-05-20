import random
import string
from src.data import email_domains


# Функция генерации данных для нового пользователя
def generate_user_data():
    def gen_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    email = gen_random_string(6) + random.choice(email_domains)
    password = gen_random_string(10)
    name = gen_random_string(10)

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    return payload
