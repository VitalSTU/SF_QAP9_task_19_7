from requests_toolbelt.multipart.encoder import MultipartEncoder
from settings import base_url
import requests


class PetFriends:
    def __init__(self):
        self.base_url = base_url

    def get_api_key(self, email: str, password: str):
        """Method makes API request. Returns request status code and user unique API key in JSON format

        :param email: user email: str
        :param password: user password: str
        :return: [Status code: int, API key: json]
        """

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: str, filter: str):
        """Method makes API request. Returns request status code and list of pets in JSON format according to filter

        :param auth_key: API key: json
        :param filter: filter: str
        :return: [Status code: int, request result: json]
        """
        headers = {
            'auth_key': auth_key,
        }
        filter = {
            'filter': filter
        }

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_new_pet_with_photo(self, auth_key: str, name: str, animal_type: str, age: int, pet_photo: str):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {
            'auth_key': auth_key,
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_new_pet_no_photo(self, auth_key: str, name: str, animal_type: str, age: int):
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {
            'auth_key': auth_key
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_set_pet_photo(self, auth_key: str, pet_id: str, pet_photo: str):
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {
            'auth_key': auth_key,
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: str, pet_id: str):
        headers = {
            'auth_key': auth_key
        }
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)
        status = res.status_code
        return status

    def put_update_pet_info(self, auth_key: str, pet_id: str, name: str, animal_type: str, age: int):
        headers = {
            'auth_key': auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

