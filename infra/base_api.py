import requests
from infra.response_wrapper import ResponseWrapper

BASE_URL = 'https://petstore.swagger.io/v2/'

class BaseApi:
    @staticmethod
    def get_api_call(end_point, body=None):
        url =  BASE_URL+ end_point
        response = requests.get(url)
        result = ResponseWrapper(response.ok, response.status_code, response.json())
        return result

    @staticmethod
    def post_api_call(end_point, body=None):
        url = BASE_URL+ end_point
        response = requests.post(url, json=body)
        result = ResponseWrapper(response.ok, response.status_code, response.json())
        return result

    def post_api_call(end_point, payload):
        url = BASE_URL + end_point
        try:
            response = requests.post(url, json=payload)
            return ResponseWrapper(response.ok, response.status_code, response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request: {e}")
            return ResponseWrapper(False, 500, {"error": str(e)})

    @staticmethod
    def delete_api_call(end_point):
        url = BASE_URL + end_point
        try:
            response = requests.delete(url)
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                data = None
            return ResponseWrapper(response.ok, response.status_code, data)

        except requests.exceptions.RequestException as e:
            print(f"Error during DELETE request: {e}")
            return ResponseWrapper(False, 500, {"error": str(e)})