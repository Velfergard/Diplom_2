import requests
import allure
import json
from src.data import API_URL


class StellarBurgerApi:

    def __init__(self, url):
        self.url = url


    @allure.step("Создаем нового пользователя")
    def create_user(self, payload):
        response = requests.post(f'{API_URL}/auth/register', json=payload)

        return response

    @allure.step("Авторизируемся под пользователем")
    def login_user(self, payload):
        response = requests.post(f'{API_URL}/auth/login', json=payload)

        return response


    @allure.step("Удаляем пользователя")
    def delete_user(self, token):
        response = requests.delete(f'{API_URL}/auth/user', headers={"Authorization": f'{token}'})

        return response


    @allure.step("Изменяем данные авторизованного пользователя")
    def update_user_data(self, token, payload):
        response = requests.patch(f'{API_URL}/auth/user', headers={"Authorization": f'{token}'}, json=payload)

        return response


    @allure.step("Получаем список ингредиентов")
    def get_ingredients(self):
        response = requests.get(f'{API_URL}/ingredients')

        return response


    @allure.step("Создаем новый заказ")
    def create_order(self, token, payload):
        response = requests.post(f'{API_URL}/orders', headers={"Authorization": f'{token}'}, json=payload)

        return response


    @allure.step("Получаем все заказы пользователя")
    def get_user_orders(self, token):
        response = requests.get(f'{API_URL}/orders', headers={"Authorization": f'{token}'})

        return response
