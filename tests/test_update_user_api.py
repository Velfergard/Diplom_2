import allure
from src import helpers


class TestUpdateUserWithAuth:

    @allure.title("Проверка изменения поля email у существующего пользователя")
    @allure.description("В тесте проверяется сценарий изменения поля email у пользователя."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_email_success200(self, gen_and_create_new_user, stellar_burger_api):
        user_data = gen_and_create_new_user[0]
        token = gen_and_create_new_user[1].json()["accessToken"]
        update_data = {
            "email": "new_" + user_data["email"]
        }

        response = stellar_burger_api.update_user_data(token, update_data)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == True
                and update_data["email"] == response.json()["user"]["email"]), f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения поля password у существующего пользователя")
    @allure.description("В тесте проверяется сценарий изменения поля password у пользователя."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_password_success200(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        token = gen_and_create_new_user[1].json()["accessToken"]
        update_data = {
            "password": "new_" + user_data["password"]
        }

        response = stellar_burger_api.update_user_data(token, update_data)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert response.json()["success"] == True, f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения поля name у существующего пользователя")
    @allure.description("В тесте проверяется сценарий изменения поля name у пользователя."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_name_success200(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        token = gen_and_create_new_user[1].json()["accessToken"]
        update_data = {
            "name": "new_" + user_data["name"]
        }

        response = stellar_burger_api.update_user_data(token, update_data)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == True
                and update_data["name"] == response.json()["user"]["name"]),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения всех полей у существующего пользователя")
    @allure.description("В тесте проверяется сценарий изменения всех полей у пользователя."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_all_data_success200(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        token = gen_and_create_new_user[1].json()["accessToken"]
        update_data = {
            "email": "new_" + user_data["email"],
            "password": "new_" + user_data["password"],
            "name" : "new_" + user_data["name"]
        }

        response = stellar_burger_api.update_user_data(token, update_data)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == True
                and update_data["email"] == response.json()["user"]["email"]
                and update_data["name"] == response.json()["user"]["name"]), \
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения поля email на уже использующийся у другого пользователя")
    @allure.description("В тесте проверяется сценарий изменения поля email на уже использующийся у другого пользователя."
                        "После выполнения теста, пользователи удаляются.")
    def test_update_user_email_that_already_exists_error403(self, stellar_burger_api, gen_and_create_new_user):
        token_one = gen_and_create_new_user[1].json()["accessToken"]

        user_two_data = helpers.generate_user_data()
        user_two = stellar_burger_api.create_user(user_two_data)
        token_two = user_two.json()["accessToken"]

        update_data = {
            "email": user_two_data["email"]
        }

        response = stellar_burger_api.update_user_data(token_one, update_data)

        assert response.status_code == 403, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "User with such email already exists" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"

        del_r_two = stellar_burger_api.delete_user(token_two)


class TestUpdateUserNoAuth:

    @allure.title("Проверка изменения поля email пользователя без авторизации")
    @allure.description("В тесте проверяется сценарий изменения поля email без авторизации."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_email_without_auth_error401(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        update_data = {
            "email": "new_" + user_data["email"]
        }

        response = stellar_burger_api.update_user_data(None, update_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "You should be authorised" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения поля password пользователя без авторизации")
    @allure.description("В тесте проверяется сценарий изменения поля password без авторизации."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_password_without_auth_error401(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        update_data = {
            "password": "new_" + user_data["password"]
        }

        response = stellar_burger_api.update_user_data(None, update_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "You should be authorised" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения поля name пользователя без авторизации")
    @allure.description("В тесте проверяется сценарий изменения поля name без авторизации."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_name_without_auth_error401(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        update_data = {
            "name": "new_" + user_data["name"]
        }

        response = stellar_burger_api.update_user_data(None, update_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "You should be authorised" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка изменения всех полей пользователя без авторизации")
    @allure.description("В тесте проверяется сценарий изменения поля name без авторизации."
                        "После выполнения теста, пользователь удаляется.")
    def test_update_user_all_data_without_auth_error401(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        update_data = {
            "email": "new_" + user_data["email"],
            "password": "new_" + user_data["password"],
            "name": "new_" + user_data["name"]
        }

        response = stellar_burger_api.update_user_data(None, update_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "You should be authorised" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"
