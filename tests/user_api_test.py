import unittest
import time
from logic.user_api import UserApi

BASE_USERNAME = "qa_test_user_"
BASE_EMAIL = "qa_tester_"

class UserApiTest(unittest.TestCase):

    def setUp(self):
        self.created_users = []

    def tearDown(self):
        for username in self.created_users:
            self._delete_user_helper(username)

    # HELPER METHODS
    def _create_unique_user(self, user_id=None):
        timestamp = str(int(time.time()))
        unique_username = BASE_USERNAME + timestamp

        payload = {
            "id": user_id if user_id is not None else int(timestamp),
            "username": unique_username,
            "firstName": "Helper",
            "lastName": "Function",
            "email": "qa_" + timestamp + "@test.com",
            "password": "password123",
            "phone": "050-2222222",
            "userStatus": 0
        }

        create_result = UserApi.create_user(payload)
        self.assertEqual(create_result.status_code, 200)
        self.created_users.append(unique_username)
        return unique_username, payload

    def _delete_user_helper(self, username):
        if username in self.created_users:
            self.created_users.remove(username)
        return UserApi.delete_user(username)

    #POST
    def test_create_user_valid_standalone(self):
        timestamp = str(int(time.time()))
        new_username = "standalone_test_" + timestamp
        user_payload = {
            "id": int(timestamp),
            "username": new_username,
            "firstName": "Standalone",
            "lastName": "Test",
            "email": "standalone@" + timestamp + ".com",
            "password": "password123",
            "phone": "050-1234567",
            "userStatus": 0
        }
        create_result = UserApi.create_user(user_payload)
        self.assertEqual(create_result.status_code, 200)

        get_result = UserApi.get_user_by_username(new_username)
        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data['username'], new_username)
        self.assertEqual(get_result.data['firstName'], "Standalone")

        UserApi.delete_user(new_username)
    #list and array the same - Just check that they work
    def test_create_multiple_users_list_success(self):
        timestamp1 = str(int(time.time()))
        timestamp2 = str(int(time.time()) + 1)

        user1_payload = {
            "id": int(timestamp1),
            "username": "list_user_1_" + timestamp1,
            "firstName": "List1",
            "email": "list1@test.com",
            "password": "p1",
            "phone": "1",
            "userStatus": 0,
            "lastName": "L1"
        }
        user2_payload = {
            "id": int(timestamp2),
            "username": "list_user_2_" + timestamp2,
            "firstName": "List2",
            "email": "list2@test.com",
            "password": "p2",
            "phone": "2",
            "userStatus": 0,
            "lastName": "L2"
        }

        list_payload = [user1_payload, user2_payload]
        create_list_result = UserApi.create_users_with_list(list_payload)

        self.assertEqual(create_list_result.status_code, 200)

        get_result_1 = UserApi.get_user_by_username(user1_payload['username'])
        self.assertEqual(get_result_1.status_code, 200)

        get_result_2 = UserApi.get_user_by_username(user2_payload['username'])
        self.assertEqual(get_result_2.status_code, 200)
        self.created_users.append(user1_payload['username'])
        self.created_users.append(user2_payload['username'])

    def test_create_multiple_users_array_success(self):
        timestamp1 = str(int(time.time()))
        timestamp2 = str(int(time.time()) + 1)

        user1_payload = {
            "id": int(timestamp1),
            "username": "array_user_1_" + timestamp1,
            "firstName": "Arr1",
            "email": "arr1@test.com",
            "password": "p1", "phone": "1", "userStatus": 0, "lastName": "L1"
        }
        user2_payload = {
            "id": int(timestamp2),
            "username": "array_user_2_" + timestamp2,
            "firstName": "Arr2",
            "email": "arr2@test.com",
            "password": "p2", "phone": "2", "userStatus": 0, "lastName": "L2"
        }

        list_payload = [user1_payload, user2_payload]
        create_array_result = UserApi.create_users_with_array(list_payload)

        self.assertEqual(create_array_result.status_code, 200)
        get_result_1 = UserApi.get_user_by_username(user1_payload['username'])

        self.assertEqual(get_result_1.status_code, 200)
        self.created_users.append(user1_payload['username'])
        self.created_users.append(user2_payload['username'])

    #GET
    def test_get_user_by_username_success(self):
        username, _ = self._create_unique_user()
        get_result = UserApi.get_user_by_username(username)

        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data['username'], username)

    def test_get_non_existent_user(self):
        username = "non_existent_user_qa"
        result = UserApi.get_user_by_username(username)

        self.assertEqual(result.ok, False)
        self.assertEqual(result.status_code, 404)

    def test_user_login_valid_credentials(self):
        password_login = "mysecretpassword1"
        username_to_test, created_payload = self._create_unique_user(user_id=10)
        created_payload['password'] = password_login

        UserApi.update_user(username_to_test, created_payload)

        login_result = UserApi.user_login(username_to_test, password_login)
        self.assertEqual(login_result.status_code, 200)
        self.assertIn('logged in user session', login_result.data['message'])

    def test_user_logout_success(self):
        password_log = "logoutpassword"
        username_to_test, created_payload = self._create_unique_user(user_id=20)
        created_payload['password'] = password_log
        UserApi.update_user(username_to_test, created_payload)

        login_result = UserApi.user_login(username_to_test, password_log)
        self.assertEqual(login_result.status_code, 200)

        logout_result = UserApi.user_logout()
        self.assertEqual(logout_result.status_code, 200)
        self.assertIn('ok', logout_result.data['message'])

    # PUT
    def test_update_user_name_success(self):
        new_first_name = "Leia"
        new_username = "updated_leia_qa"
        original_username, payload_base = self._create_unique_user()

        payload_base['firstName'] = new_first_name
        payload_base['username'] = new_username

        update_result = UserApi.update_user(original_username, payload_base)
        self.assertEqual(update_result.status_code, 200)

        if original_username in self.created_users:
            self.created_users.remove(original_username)
        self.created_users.append(new_username)

        get_result = UserApi.get_user_by_username(new_username)
        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data['firstName'], new_first_name)
        self.assertEqual(get_result.data['username'], new_username)

    #DELETE
    def test_delete_user_success(self):
        username, _ = self._create_unique_user()

        delete_result = UserApi.delete_user(username)
        self.assertEqual(delete_result.status_code, 200)

        if username in self.created_users:
            self.created_users.remove(username)

        verify_delete_result = UserApi.get_user_by_username(username)
        self.assertEqual(verify_delete_result.status_code, 404)

    def test_delete_non_existent_user(self):
        non_existent_username = "non_existent_user_for_delete_99999"
        delete_result = UserApi.delete_user(non_existent_username)

        self.assertEqual(delete_result.ok, False)
        self.assertEqual(delete_result.status_code, 404)