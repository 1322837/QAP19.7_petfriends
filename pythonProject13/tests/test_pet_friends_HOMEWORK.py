from api import PetFriends
from settings import valid_email, valid_password
import os
import uuid

pf = PetFriends()

# №1: Негативный тест на получение ключа для при использовании некорректных данных
def test_get_api_key_for_invalid_user(email='invalid_email', password='invalid_password'):

    status, result = pf.get_api_key(email, password)

    assert status != 200


# №2: Позитивный тест на добавление нового питомца без фото
def test_add_new_pet_simple(name='Кот', animal_type='Пёс',age='44',):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age,)

    assert status == 200
    assert result['name'] == name


# №3: Позитивный тест на добавление фото к предыдущему питомцу, если список питомцев пустой то оно создает нового и добавляет к нему фото
def test_add_photo_of_pet(pet_photo='images/cat1.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Пёс", "кот", "34",)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200


# №4: Негативный тест на добавление фото к питомцу со случайным UUID
def test_add_photo_to_random_pet(pet_photo='images/cat1.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_id = str(uuid.uuid1())
    print(pet_id)
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status != 200


# №5: Негативный тест на добавление фото в неправильном расширении
def test_add_photo_of_pet_wrong_ext(pet_photo='images/cat1.txt'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Пёс", "кот", "34",)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status != 200


# №6: Негативный тест на добавление нового питомца с пустыми параметрами
def test_add_new_pet_simple_empty_fields(name='', animal_type='',age=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age,)

    assert status != 200


# №7: Негативный тест на добавление нового питомца с различными символами в параметрах
def test_add_new_pet_simple_symbols(name="""!@#$%^&*(){}[]"№:;?*,/|\:"'><?/""", animal_type="""!@#$%^&*(){}[]"№:;?*,/|\:"'><?/""",age='100'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age,)

    assert status != 200


# №8: Негативный тест на добавление нового питомца с пустыми параметрами
def test_add_new_pet_simple_incorrect_age(name='Кот', animal_type='Пёс',age='definitely_not_a_number'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age,)

    assert status != 200


# №9: Негативный тест на добавление нового питомца со слишком большим возрастом
def test_add_new_pet_simple_long_number(name='Кот', animal_type='Пёс',age=f'{10**1000}',):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age,)

    assert status != 200


# №10: Негативный тест на добавление нового питомца с неправильным ключом
def test_add_new_pet_simple_wrong_key(name='Кот', animal_type='Пёс',age='44',):

    auth_key = {'key': 'definitely_not_auth_key'}

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age,)

    assert status != 200
