from api import PetFriends
from settings import *
from termcolor import colored

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


def test_positive_get_list_of_all_pets_valid_key(filter='', email=valid_email, password=valid_password):
    """Method makes API request. Returns request status code and list of all pets in JSON format according to filter

    :param filter:
    :return:
    """
    _, auth_key = pets.get_api_key(email, password)
    status, result = pets.get_list_of_pets(auth_key['key'], filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_positive_post_create_new_pet_with_photo(email=valid_email, password=valid_password):
    """Method makes API request for new pet with photo creation.

    :return:
    """
    _, auth_key = pets.get_api_key(email, password)
    status, result = pets.post_add_new_pet_with_photo(auth_key['key'],
                                                      name='Barsic',
                                                      animal_type='Demonic Cat',
                                                      age=13,
                                                      pet_photo=pet1photo
                                                      )
    assert status == 200
    assert result['name'] == 'Barsic'


def test_positive_get_list_of_my_pets_valid_key(filter='my_pets', email=valid_email, password=valid_password):
    """Method makes API request. Returns request status code and list of my pets in JSON format according to filter

    :param filter:
    :return:
    """
    _, auth_key = pets.get_api_key(email, password)
    status, result = pets.get_list_of_pets(auth_key['key'], filter)
    # print('\n My pets quantity =', len(result['pets']))
    assert status == 200
    assert len(result['pets']) > 0


def test_positive_delete_pet_valid_id(email=valid_email, password=valid_password):
    """Method deletes last pet

    :return:
    """
    _, auth_key = pets.get_api_key(email, password)
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


def test_positive_post_create_new_pet_no_photo(email=valid_email, password=valid_password):
    """Method makes API request for new pet with no photo creation.

    :return:
    """
    _, auth_key = pets.get_api_key(email, password)
    status, result = pets.post_add_new_pet_no_photo(auth_key['key'],
                                                    name='Bobik',
                                                    animal_type='Angel Dog',
                                                    age=7
                                                    )
    assert status == 200
    assert result['name'] == 'Bobik'


def test_positive_post_set_pet_photo(email=valid_email, password=valid_password):
    """Method sets photo for last pet

    :return:
    """
    _, auth_key = pets.get_api_key(email, password)
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
    if len1 > 0:
        # first_pet_id = pets_list[len(pets_list) - 1]['id']
        last_pet_id = pets_list[0]['id']
        status, result = pets.post_set_pet_photo(auth_key['key'],
                                                 pet_id=last_pet_id,
                                                 pet_photo=pet3photo)
        edited_pet_id = result['id']
        assert status == 200
        assert edited_pet_id == last_pet_id
    else:
        raise Exception('There is no pets in list to be updated')


def test_positive_put_update_pet_info(email=valid_email, password=valid_password):
    _, auth_key = pets.get_api_key(email, password)
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)
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
def test_negative_get_api_key_for_valid_user(email=valid_email, password=invalid_password):
    #  1 Негативный тест - Попытка авторизации (получения API key)) с валидным email и невалидным password

    status, result = pets.get_api_key(email, password)
    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 403


def test_negative_get_list_of_my_pets_valid_key(filter='my_pets',
                                                auth_key="<script>alert('test script')</script>"):
    #  2 Негативный тест - Попытка получения списка моих питомцев по программому коду вместо API key
    #                       <script>alert('test script')</script>

    status, result = pets.get_list_of_pets(auth_key, filter)
    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 403


def test_negative_get_list_of_pets_invalid_filter(filter='not_valid_filter',
                                                  email=valid_email,
                                                  password=valid_password):
    #  3 Негативный тест - Попытка получения списка питомцев по невалидному парамерту filter = 'not_valid_filter'

    _, auth_key = pets.get_api_key(email, password)
    status, result = pets.get_list_of_pets(auth_key['key'], filter)
    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 500


def test_negative_delete_pet_invalid_id(email=valid_email, password=valid_password):
    #  4 Негативный тест - Попытка удаления питомца с невалидным id

    _, auth_key = pets.get_api_key(email, password)

    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len1 = len(pets_list)

    status = pets.delete_pet(auth_key['key'],
                             pet_id='invalid_pet_id'
                             )

    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    pets_list = answer['pets']
    len2 = len(pets_list)

    assert status == 404
    assert len1 == len2


def test_negative_delete_anothers_pet_valid_id(email=valid_email, password=valid_password):
    # 5 Негативный тест - Попытка удаления чужого питомца с валидным id

    _, auth_key = pets.get_api_key(email, password)

    # Find last pet id
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='')
    all_pets_list = answer['pets']
    last_pet_id = all_pets_list[0]['id']

    # Find my last pet id
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    my_last_pet_id = my_pets_list[0]['id']

    if last_pet_id != my_last_pet_id:
        # Test number of prts in database
        len1 = len(all_pets_list)

        status = pets.delete_pet(auth_key['key'],
                                 pet_id=last_pet_id
                                 )

        # Test number of prts in database
        _, answer = pets.get_list_of_pets(auth_key['key'], filter='')
        all_pets_list = answer['pets']
        len2 = len(all_pets_list)

        assert status == 403
        assert len1 == len2
    else:
        print(colored('\n Last pet is yours. Test can not be processed. '
                      'Be sure last pet in database is not yours', 'red'))


def test_negative_post_create_new_pet_with_bad_photo(email=valid_email, password=valid_password):
    # 6 Негативный тест - Попытка добавления питомца с запоротой фотографией
    # Поскольку в POST-запросе на создание питомца с фотографией есть бак с типом поля "age",
    # то просто пишем в него строковое значение, чтобы баг не блокировал данный тест

    _, auth_key = pets.get_api_key(email, password)

    # Look how many pets before test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)

    status, result = pets.post_add_new_pet_with_photo(auth_key['key'],
                                                      name='Pupsic',
                                                      animal_type='Baby lion',
                                                      age='1',
                                                      pet_photo=invalid_photo
                                                      )

    # Look how many pets after test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)

    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 500
    assert len1 == len2


def test_negative_post_create_new_pet_with_txt_photo(email=valid_email, password=valid_password):
    # 7 Негативный тест - Попытка добавления питомца с txt-файлом вместо фотографии
    # Поскольку в POST-запросе на создание питомца с фотографией есть бак с типом поля "age",
    # то просто пишем в него строковое значение, чтобы баг не блокировал данный тест

    _, auth_key = pets.get_api_key(email, password)

    # Look how many pets before test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)

    status, result = pets.post_add_new_pet_with_photo(auth_key['key'],
                                                      name='Chizhic',
                                                      animal_type='Solovey',
                                                      age='1',
                                                      pet_photo=text_photo
                                                      )

    # Look how many pets after test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)

    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 500
    assert len1 == len2


def test_negative_post_create_new_pet_no_photo_name_type_integer(email=valid_email, password=valid_password):
    #  8 Негативный тест - Попытка добавления питомца без фото с числовым значением имени

    _, auth_key = pets.get_api_key(email, password)

    # Look how many pets before test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)

    status, result = pets.post_add_new_pet_no_photo(auth_key['key'],
                                                    name=313,
                                                    animal_type='Snake',
                                                    age=7
                                                    )

    # Look how many pets after test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)

    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 500
    assert len1 == len2


def test_negative_post_create_new_pet_no_photo_age_is_under_zero(email=valid_email, password=valid_password):
    #  9 Негативный тест - Попытка добавления питомца без фото с отрицательным возрастом

    _, auth_key = pets.get_api_key(email, password)

    # Look how many pets before test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)

    status, result = pets.post_add_new_pet_no_photo(auth_key['key'],
                                                    name='Schrodinger',
                                                    animal_type="Schrodinger's cat",
                                                    age=-3
                                                    )

    # Look how many pets after test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)

    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 500
    assert len1 == len2


def test_negative_post_create_new_pet_no_photo_long_name(email=valid_email, password=valid_password):
    # 10 Негативный тест - Попытка добавления питомца без фото с очень длинным именем > 255 символов

    _, auth_key = pets.get_api_key(email, password)

    # Look how many pets before test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len1 = len(my_pets_list)

    status, result = pets.post_add_new_pet_no_photo(auth_key['key'],
                                                    name=long_name,
                                                    animal_type="Voina i mir",
                                                    age=150
                                                    )

    # Look how many pets after test
    _, answer = pets.get_list_of_pets(auth_key['key'], filter='my_pets')
    my_pets_list = answer['pets']
    len2 = len(my_pets_list)

    if type(result) is str:
        p1 = result.find('<p>')
        p2 = result.find('</p>')
        print(colored('\n' + result[p1 + 3:p2], 'red'))
    assert status == 500
    assert len1 == len2
