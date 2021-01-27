from api import PetFriends
from settings import *
# import requests
# import json

pets = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Method makes API request. Returns request status code and user unique API key in JSON format

    :param email:
    :param password:
    :return:
    """
    status, result = pets.get_api_key(email, password)
    print('\nKey =', result['key'])
    # Key = 8257cd29edc72a6b23e10a931ae5dc56fe88a66270ac04ef974555da
    assert status == 200
    assert 'key' in result
