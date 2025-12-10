from infra.base_api import BaseApi

class UserApi():

    @staticmethod
    def get_user_by_username(username):
        return BaseApi.get_api_call(f'user/{username}')

    @staticmethod
    def create_user(user_body):
        return BaseApi.post_api_call('user', user_body)

    @staticmethod
    def create_users_with_list(list_of_users_payload):
        return BaseApi.post_api_call('user/createWithList', list_of_users_payload)

    @staticmethod
    def create_users_with_array(array_of_users_payload):
        return BaseApi.post_api_call('user/createWithArray', array_of_users_payload)

    @staticmethod
    def update_user(username_to_update, updated_payload):
        return BaseApi.put_api_call(f'user/{username_to_update}', updated_payload)

    @staticmethod
    def delete_user(username):
        return BaseApi.delete_api_call(f'user/{username}')

    @staticmethod
    def user_login(username, password):
        path = f'user/login?username={username}&password={password}'
        return BaseApi.get_api_call(path)

    @staticmethod
    def user_logout():
        return BaseApi.get_api_call('user/logout')
