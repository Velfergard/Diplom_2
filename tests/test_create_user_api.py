import pytest
import allure
from src import helpers


class TestCreateUserApi:

    @allure.title("Проверка создания нового (уникального) пользователя")
    @allure.description("В тесте проверяется сценарий создания нового уникального пользователя."
                        "После выполнения теста, данный пользователь удаляется.")
    def test_create_unique_user_success200(self, gen_and_create_new_user):
        data = gen_and_create_new_user[0]
        user = gen_and_create_new_user[1]

        assert user.status_code == 200, f"Некорректный статус-код ответа: {user.status_code}"
        assert (user.json()["success"] == True
                and data["email"] == user.json()["user"]["email"]
                and data["name"] == user.json()["user"]["name"]
                and ("accessToken" in user.json() and len(user.json()["accessToken"]) > 0)
                and ("refreshToken" in user.json() and len(user.json()["refreshToken"]) > 0)),\
                f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка создания нового пользователя по данным уже существующего пользователя")
    @allure.description("В тесте проверяется сценарий создания пользователя-дубликата."
                        "После выполнения теста, данный пользователь-исходник удаляется.")
    def test_create_user_with_existed_data_error403(self, stellar_burger_api, gen_and_create_new_user):
        data = gen_and_create_new_user[0]
        response = stellar_burger_api.create_user(data)

        assert response.status_code == 403, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "User already exists" == response.json()["message"]), f"Тело ответа не соответствует ожидаемому"


    @allure.title("Проверка создания пользователя без обязательных реквизитов")
    @allure.description("В тесте проверяется сценарий создания нового пользователя без передачи обязательных реквизитов."
                        "После выполнения теста, данный пользователь удаляется (если был создан по ошибке).")

    @pytest.mark.parametrize('user_data', [
        ["", "qwerty1234", "Test User19"],
        ["Test_email19300425@mail.ru", "", "Test User19"],
        ["Test_email19300425@yandex.ru", "qwerty1234", ""]
    ])
    def test_create_user_without_required_fields_error403(self, user_data, stellar_burger_api):
        data = {
            "email": user_data[0],
            "password": user_data[1],
            "name": user_data[2]
        }

        response = stellar_burger_api.create_user(data)

        assert response.status_code == 403, f"Некорректный статус-код ответа: {response.status_code}"
        assert (response.json()["success"] == False
                and "Email, password and name are required fields" == response.json()["message"]),\
                f"Тело ответа не соответствует ожидаемому"

        try:
            del_r = stellar_burger_api.delete_user(response.json()["accessToken"])
            assert del_r.status_code == 202
            assert del_r.json()["success"] == True

        except:
            pass
