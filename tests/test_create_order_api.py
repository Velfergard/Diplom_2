import pytest
import allure


class TestCreateOrderWithAuth:

    @allure.title("Проверка создания нового заказа")
    @allure.description("В тесте проверяется позитивный сценарий создания нового заказа под авторизованным юзером."
                        "После выполнения теста, пользователь удаляется.")
    def test_create_order_with_ingredients_success200(self, create_new_order):
        order = create_new_order

        assert order.status_code == 200, f"Некорректный статус-код ответа: {order.status_code}"
        assert (order.json()["success"] == True
                and order.json()["order"]["number"] > 0), f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка создания нового заказа без ингредиентов")
    @allure.description("В тесте проверяется негативный сценарий создания нового заказа без ингредиентов."
                        "После выполнения теста, пользователь удаляется.")

    @pytest.mark.parametrize("order_data", [{"ingredients": None}, {"ingredients": ""}, {}])
    def test_create_order_without_ingredients_error400(self
                                                       , order_data
                                                       , stellar_burger_api
                                                       , gen_and_create_new_user
                                                       , get_ingredients
                                                       ):
        user = gen_and_create_new_user[1]
        token = user.json()["accessToken"]

        response = stellar_burger_api.create_order(token, order_data)

        assert response.status_code == 400, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "Ingredient ids must be provided" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка создания нового заказа с некорректным id ингредиента")
    @allure.description("В тесте проверяется негативный сценарий создания нового заказа с некорректным id ингредиента."
                        "После выполнения теста, пользователь удаляется.")
    def test_create_order_with_incorrect_ingredient_error500(self
                                                             , stellar_burger_api
                                                             , gen_and_create_new_user
                                                             , get_ingredients
                                                             ):
        user = gen_and_create_new_user[1]
        token = user.json()["accessToken"]
        order_data = {
            "ingredients": "test_ingredient123!"
        }

        response = stellar_burger_api.create_order(token, order_data)

        assert response.status_code == 500, f"Некорректный статус-код ответа: {response.status_code}"
        assert "Internal Server Error" in response.text, f"Тело ответа не соответствует ожидаемому"


class TestCreateOrderNoAuth:

    # Тест падает по ошибке из-за бага, что под неавторизованным юзером можно создать заказ
    @allure.title("Проверка создания нового заказа без авторизации")
    @allure.description("В тесте проверяется негативный сценарий создания нового заказа без авторизации."
                        "После выполнения теста, пользователь удаляется.")
    def test_create_order_with_ingredients_without_auth_error401(self
                                                      , stellar_burger_api
                                                      , get_ingredients
                                                      ):
        token = None
        order_data = {
            "ingredients": [get_ingredients[2], get_ingredients[3]]
        }

        response = stellar_burger_api.create_order(token, order_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "You should be authorised" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка создания нового заказа без ингредиентов без авторизации")
    @allure.description("В тесте проверяется негативный сценарий создания нового заказа без ингредиентов без авторизации."
                        "После выполнения теста, пользователь удаляется.")

    @pytest.mark.parametrize("order_data", [{"ingredients": None}, {"ingredients": ""}, {}])
    def test_create_order_without_ingredients_without_auth_error400(self, order_data, stellar_burger_api):
        token = None

        response = stellar_burger_api.create_order(token, order_data)

        assert response.status_code == 400, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "Ingredient ids must be provided" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"
