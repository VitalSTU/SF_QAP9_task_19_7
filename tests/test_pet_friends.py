from api import PetFriends
from settings import *
# import requests
# import json

pets = PetFriends()


def test_positive_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Method makes API request. Returns request status code and user unique API key in JSON format

    :param email:
    :param password:
    :return:
    """
    status, result = pets.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_positive_get_list_of_all_pets_valid_key(filter=''):
    """Method makes API request. Returns request status code and list of all pets in JSON format according to filter

    :param filter:
    :return:
    """
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    status, result = pets.get_list_of_pets(auth_key['key'], filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_positive_post_create_new_pet_with_photo():
    """Method makes API request for new pet with photo creation.

    :return:
    """
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    status, result = pets.post_add_new_pet_with_photo(auth_key['key'],
                                                      name='Barsic',
                                                      animal_type='Demonic Cat',
                                                      age='13',
                                                      pet_photo=pet1photo
                                                      )
    assert status == 200
    assert result['name'] == 'Barsic'


def test_positive_get_list_of_my_pets_valid_key(filter='my_pets'):
    """Method makes API request. Returns request status code and list of my pets in JSON format according to filter

    :param filter:
    :return:
    """
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    status, result = pets.get_list_of_pets(auth_key['key'], filter)
    # print('\n My pets quantity =', len(result['pets']))
    assert status == 200
    assert len(result['pets']) > 0


def test_positive_delete_pet():
    """Method deletes last pet

    :return:
    """
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
    if len1 > 0:
        last_pet_id = pets_list[0]['id']
        status = pets.delete_pet(auth_key['key'],
                                 pet_id=last_pet_id
                                 )
        _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
        pets_list = answer['pets']
        len2 = len(pets_list)
        assert status == 200
        assert (len1 - len2) == 1
    else:
        raise Exception('There is no pets in list to be deleted')


def test_positive_post_create_new_pet_no_photo():
    """Method makes API request for new pet with no photo creation.

    :return:
    """
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    status, result = pets.post_add_new_pet_no_photo(auth_key['key'],
                                                    name='Bobik',
                                                    animal_type='Angel Dog',
                                                    age=7
                                                    )
    assert status == 200
    assert result['name'] == 'Bobik'


def test_positive_post_set_pet_photo():
    """Method sets photo for last pet

    :return:
    """
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
    if len1 > 0:
        # first_pet_id = pets_list[len(pets_list) - 1]['id']
        last_pet_id = pets_list[0]['id']
        # print('\n Last pet id =', last_pet_id)
        status, result = pets.post_set_pet_photo(auth_key['key'],
                                                 pet_id=last_pet_id,
                                                 pet_photo=pet3photo)
        edited_pet_id = result['id']
        # print('\n Edited pet id =', edited_pet_id)
        assert status == 200
        assert edited_pet_id == last_pet_id
    else:
        raise Exception('There is no pets in list to be updated')


def test_positive_put_update_pet_info():
    _, auth_key = pets.get_api_key(valid_email, valid_password)
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
    # print('\n', len1)
    if len1 > 0:
        last_pet_id = pets_list[0]['id']
        status, result = pets.put_update_pet_info(auth_key['key'],
                                                  pet_id=last_pet_id,
                                                  name='Sonic',
                                                  animal_type='Supersonic Hedgehog',
                                                  age=15
                                                  )
        edited_pet_id = result['id']
        assert status == 200
        assert edited_pet_id == last_pet_id
    else:
        raise Exception('There is no pets in list to be updated')

# 19.7 Practice:

# Негативный тест - Попытка авторизации (получения API key)) с валидным email и невалидным password
# Негативный тест - Попытка получения списка всех питомцев по невалидному API key
# Негативный тест - Попытка получения списка моих питомцев по невалидному API key
# Негативный тест - Попытка получения списка питомцев по невалидному парамерту filter = 'not_valid_filter'
# Негативный тест - Попытка удаления питомца с невалидным id
# Негативный тест - Попытка удаления чужого питомца с валидным id
# Негативный тест - Попытка добавления питомца с фотографией 190 мегабайт
# Негативный тест - Попытка добавления питомца с txt-файлом вместо фотографии
# Негативный тест - Попытка добавления питомца с отрицательным возрастом
# Негативный тест - Попытка добавления питомца со строковым значением возраста возрастом
# Негативный тест - Попытка добавления питомца с очень длинным именем > 255 символов

# Готовые тест-кейсы разместите на GitHub и пришлите ссылку.
