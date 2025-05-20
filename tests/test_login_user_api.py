import pytest
import allure


class TestLoginUserApi:

    @allure.title("Проверка авторизации пользователя с корректными данными")
    @allure.description("В тесте проверяется сценарий корректной авторизации пользователя."
                        "После выполнения теста, пользователь удаляется.")
    def test_login_user_with_correct_data_success200(self, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        response = stellar_burger_api.login_user(login_data)

        assert response.status_code == 200, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == True
                and user_data["email"] == response.json()["user"]["email"]
                and user_data["name"] == response.json()["user"]["name"]
                and ("accessToken" in response.json() and len(response.json()["accessToken"]) > 0)
                and ("refreshToken" in response.json() and len(response.json()["refreshToken"]) > 0)), \
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка авторизации пользователя с некорректным логином")
    @allure.description("В тесте проверяется сценарий авторизации пользователя с использованием некорректных логинов."
                        "После выполнения теста, пользователь удаляется.")

    @pytest.mark.parametrize("login", ["", None, "null"])
    def test_login_user_with_incorrect_login_error401(self, login, gen_and_create_new_user, stellar_burger_api):
        user_data = gen_and_create_new_user[0]
        login_data = {
            "email": login,
            "password": user_data["password"]
        }

        response = stellar_burger_api.login_user(login_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "email or password are incorrect" == response.json()["message"]), \
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка авторизации пользователя с некорректным паролем")
    @allure.description("В тесте проверяется сценарий авторизации пользователя с использованием некорректных паролей."
                        "После выполнения теста, пользователь удаляется.")

    @pytest.mark.parametrize("password", ["", None, "null"])
    def test_login_user_with_incorrect_password_error401(self, password, stellar_burger_api, gen_and_create_new_user):
        user_data = gen_and_create_new_user[0]
        login_data = {
            "email": user_data["email"],
            "password": password
        }

        response = stellar_burger_api.login_user(login_data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "email or password are incorrect" == response.json()["message"]), \
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка авторизации пользователя без обязательных полей")
    @allure.description("В тесте проверяется негативный сценарий авторизации пользователя,"
                        "когда не передаются обязательные поля в теле запроса.")

    @pytest.mark.parametrize("data", [{"email": "test123@yandex.ru"}, {"password": "qaz123"}, {}])
    def test_login_user_without_required_fields_error401(self, data, stellar_burger_api):
        response = stellar_burger_api.login_user(data)

        assert response.status_code == 401, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "email or password are incorrect" == response.json()["message"]), \
                f"Тело ответа не соответствует ожидаемому"
