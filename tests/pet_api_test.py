import unittest
import time
from logic.pet_api import PetApi

class PetApiTest(unittest.TestCase):

    def setUp(self):
        self.created_pet_ids = []

    def tearDown(self):
        for pet_id in self.created_pet_ids:
            self._delete_pet_helper(pet_id)

    #HELPER METHODS

    def _create_unique_pet(self, status="available"):
        unique_id = int(time.time() * 1000)

        pet_payload = {
            "id": unique_id,
            "category": {"id": 1, "name": "dogs"},
            "name": f"TestDog_{unique_id}",
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "test"}],
            "status": status
        }

        create_result = PetApi.create_pet(pet_payload)
        self.assertEqual(create_result.status_code, 200)

        self.created_pet_ids.append(unique_id)

        return unique_id, pet_payload

    def _delete_pet_helper(self, pet_id):
        if pet_id in self.created_pet_ids:
            self.created_pet_ids.remove(pet_id)
        return PetApi.delete_pet(pet_id)

    def test_create_pet_valid_request(self):
        #POST
        pet_id, expected_payload = self._create_unique_pet()
        get_result = PetApi.get_pet_by_id(pet_id)

        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data['id'], pet_id)
        self.assertEqual(get_result.data['name'], expected_payload['name'])

    def test_get_pet_by_id_valid_id(self):
        #GET
        pet_id, expected_payload = self._create_unique_pet()
        get_result = PetApi.get_pet_by_id(pet_id)

        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data['id'], pet_id)

    def test_update_existing_pet_valid_update(self):
        #PUT
        new_status = "sold"
        new_name = "LeiaTheSoldDog"

        pet_id, original_payload = self._create_unique_pet(status="available")
        original_payload['status'] = new_status
        original_payload['name'] = new_name
        update_result = PetApi.update_pet(original_payload)
        self.assertEqual(update_result.status_code, 200)

        get_result = PetApi.get_pet_by_id(pet_id)
        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data['status'], new_status)

    def test_get_pets_by_status_success(self):
        status_to_check = "available"
        pet_id, _ = self._create_unique_pet(status=status_to_check)
        find_result = PetApi.find_pets_by_status(status_to_check)
        self.assertEqual(find_result.status_code, 200)

        pet_ids_in_response = [pet['id'] for pet in find_result.data]
        self.assertIn(pet_id, pet_ids_in_response)

    def test_delete_pet_valid_id(self):
        #DELETE
        pet_id, _ = self._create_unique_pet()
        delete_result = PetApi.delete_pet(pet_id)
        self.assertEqual(delete_result.status_code, 200)
        if pet_id in self.created_pet_ids:
            self.created_pet_ids.remove(pet_id)
        verify_delete_result = PetApi.get_pet_by_id(pet_id)
        self.assertEqual(verify_delete_result.status_code, 404)

    def test_get_pet_by_non_existing_id_failure(self):
        non_existing_id = 999999999999
        get_result = PetApi.get_pet_by_id(non_existing_id)

        self.assertEqual(get_result.status_code, 404)
        self.assertIn("Pet not found", get_result.data.get('message', ''))

    def test_delete_pet_non_existing_id_failure(self):
        non_existing_id = 888888888888
        delete_result = PetApi.delete_pet(non_existing_id)
        self.assertEqual(delete_result.status_code, 404)