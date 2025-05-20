import allure


class TestGetUserOrdersWithAuth:

    @allure.title("Проверка получения заказов авторизованного пользователя")
    @allure.description("В тесте проверяется сценарий получения заказов под пользователем, у которого нет своих заказов."
                        "После выполнения теста, пользователь удаляется.")
    def test_get_user_orders_without_orders_success200(self, stellar_burger_api, gen_and_create_new_user):
        user = gen_and_create_new_user[1]
        token = user.json()["accessToken"]

        response = stellar_burger_api.get_user_orders(token)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == True
                and "orders" in response.json()
                and response.json()["total"] >= 0
                and response.json()["totalToday"] >= 0), f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка получения заказов авторизованного пользователя")
    @allure.description("В тесте проверяется сценарий получения заказов под пользователем, у которого есть свои заказы."
                        "После выполнения теста, пользователь удаляется.")
    def test_get_user_orders_with_orders_success200(self
                                                    , stellar_burger_api
                                                    , gen_and_create_new_user
                                                    , get_ingredients
                                                    ):

        user = gen_and_create_new_user[1]
        token = user.json()["accessToken"]
        order_data = {
            "ingredients": [get_ingredients[4], get_ingredients[5]]
        }
        order = stellar_burger_api.create_order(token, order_data)

        response = stellar_burger_api.get_user_orders(token)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == True
                and len(response.json()["orders"]) > 0
                and response.json()["orders"][0]["ingredients"] == order_data["ingredients"]
                and response.json()["orders"][0]["number"] == order.json()["order"]["number"]
                and response.json()["total"] >= 0
                and response.json()["totalToday"] >= 0), f"Тело ответа не соответствует ожидаемому"

        del_user = stellar_burger_api.delete_user(token)


class TestGetUserOrdersNoAuth:

    @allure.title("Проверка получения заказов без авторизации")
    @allure.description("В тесте проверяется негативный сценарий получения заказов без авторизации.")
    def test_get_user_orders_without_orders_without_auth_error401(self, stellar_burger_api):
        token = None

        response = stellar_burger_api.get_user_orders(token)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
               and "You should be authorised" == response.json()["message"]), \
                f"Тело ответа не соответствует ожидаемому"
