import requests
from infra.response_wrapper import ResponseWrapper

class BaseApi:
    @staticmethod
    def get_api_call(end_point, body=None):
        url = f'https://petstore.swagger.io/v2/{end_point}'
        response = requests.get(url)
        result = ResponseWrapper(response.ok, response.status_code, response.json())
        return result

    @staticmethod
    def post_api_call(end_point, body=None):
        url = f'https://petstore.swagger.io/v2/{end_point}'
        response = requests.post(url, json=body)
        result = ResponseWrapper(response.ok, response.status_code, response.json())
        return result