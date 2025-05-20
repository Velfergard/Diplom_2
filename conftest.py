import pytest
import random
from src import helpers
from src.data import API_URL
from src.stellar_burger_api import StellarBurgerApi


# Фикстура для создания объекта класса API
@pytest.fixture()
def stellar_burger_api():

    return StellarBurgerApi(API_URL)


# Фикстура для генерации и создания нового пользователя
@pytest.fixture()
def gen_and_create_new_user(stellar_burger_api):
    user_data = helpers.generate_user_data()
    user = stellar_burger_api.create_user(user_data)
    yield user_data, user

    stellar_burger_api.delete_user(user.json()["accessToken"])


# Фикстура для получения списка айди ингредиентов
@pytest.fixture()
def get_ingredients(stellar_burger_api):
    ingredients_list = []

    for ingredient in stellar_burger_api.get_ingredients().json()["data"]:
        ingredients_list.append(ingredient["_id"])

    return ingredients_list


# Фикстура для создания заказа
@pytest.fixture()
def create_new_order(stellar_burger_api, gen_and_create_new_user, get_ingredients):
    token = gen_and_create_new_user[1].json()["accessToken"]
    ingredients = random.choices(get_ingredients, k=3)
    order_data = {
        "ingredients": ingredients
    }
    order = stellar_burger_api.create_order(token, order_data)

    return order
