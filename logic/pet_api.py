from infra.base_api import BaseApi

class PetApi():

    @staticmethod
    def create_pet(pet_payload):
        # ה-Payload נשלח בגוף הבקשה
        return BaseApi.post_api_call('pet', pet_payload)

    @staticmethod
    def get_pet_by_id(pet_id):
        return BaseApi.get_api_call(f'pet/{pet_id}')

    @staticmethod
    def update_pet(pet_payload):
        return BaseApi.put_api_call('pet', pet_payload)

    @staticmethod
    def delete_pet(pet_id):
        return BaseApi.delete_api_call(f'pet/{pet_id}')

    @staticmethod
    def find_pets_by_status(status):
        return BaseApi.get_api_call(f'pet/findByStatus?status={status}')