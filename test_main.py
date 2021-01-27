'''This module contains tests for main.py, users.py and user_status.py'''
# pylint: disable=W0621

import os
from unittest.mock import patch
from unittest.mock import mock_open
import copy
import pytest
import main
import users
import user_status


# fixtures


@pytest.fixture
def tolby():
    '''return tolby'''
    user_id = 'Cool_kid187'
    email = 'mommasboy2001@gmail.com'
    user_name = 'Tolby'
    user_last_name = 'Bryant'
    params = [user_id, email, user_name, user_last_name]

    tolby = users.Users(*params)
    return tolby


@pytest.fixture
def eve():
    '''return eve'''
    line1 = ['evmiles97', 'eve.miles@uw.edu', 'Eve', 'Miles']
    eve = users.Users(*line1)

    return eve


@pytest.fixture
def dave():
    '''return dave'''
    line2 = ['dave03', 'david.yuen@gmail.com', 'David', 'Yuen']
    dave = users.Users(*line2)

    return dave


@pytest.fixture
def collection():
    '''return empty UserCollection'''
    collection = users.UserCollection()

    return collection


@pytest.fixture()
def database(eve, dave, tolby):
    '''return user_database'''
    # database = {user_id: user_obj}
    database = {'evmiles97': eve,
                'dave03': dave,
                'Cool_kid187': tolby,
                }

    return database


@pytest.fixture
def impeach():
    '''return impeach'''
    status_id = 'XKPiC6*iW!H3#6'
    user_id = 'Hardline_Dem173'
    status_text = 'Impeach Trump!'
    params = [status_id, user_id, status_text]

    impeach = user_status.UserStatus(*params)

    return impeach


@pytest.fixture
def stolen():
    '''return stolen'''
    status_id = 'RbLr8!yCs*3DSC'
    user_id = 'Hardline_GOP173'
    status_text = 'The election was stolen from Trump!'
    params = [status_id, user_id, status_text]

    status = user_status.UserStatus(*params)

    return status


@pytest.fixture
def flat():
    '''return flat'''
    status_id = 'G5Yz%#kTda&TFt'
    user_id = 'The_Real_Bill_Nye'
    status_text = 'The earth is flat!'
    params = [status_id, user_id, status_text]

    status = user_status.UserStatus(*params)

    return status


@pytest.fixture()
def status_database(impeach, stolen, flat):
    '''return status database'''
    # database = {status_id: status_obj}
    database = {'XKPiC6*iW!H3#6': impeach,
                'RbLr8!yCs*3DSC': stolen,
                'G5Yz%#kTda&TFt': flat,
                }

    return database


@pytest.fixture
def status_collection():
    '''return empty status_collection'''
    collection = user_status.UserStatusCollection()

    return collection


@pytest.fixture()
def csv_database(eve, dave):
    '''return database with users in accounts.csv 2/3'''
    # database = {user_id: user_obj}
    database = {'evmiles97': eve,
                'dave03': dave
                }

    return database


@pytest.fixture
def csv_collection(csv_database):
    '''return a user collection preloaded with csv_database'''
    collection = users.UserCollection()

    collection.database = csv_database

    return collection


@pytest.fixture
def filename():
    '''return accounts.csv string'''
    filename = 'accounts.csv'

    return filename


@pytest.fixture
def temp_file():
    '''create an empty file and return the filename'''
    filename = 'test.csv'

    with open(filename, 'w'):
        pass

    return filename


def clean_temp_file(filename='test.csv'):
    '''delete a file'''

    os.remove(filename)


# user tests


def test_users_init(tolby):
    '''test users_init'''
    assert tolby.email == 'mommasboy2001@gmail.com'


def test_user_collection_init(collection):
    '''test UsersCollection init'''
    assert collection.database == {}


def test_user_collection_add_user(collection, database):
    '''test UserCollection add_user'''
    collection.database = database
    new_user = ['Big****123', 'AElrick@BTISolutions.com', 'My', 'Secret']
    assert collection.add_user(*new_user) is True


def test_user_collection_add_user_reject_existing(collection, database):
    '''test add_user rejects existing users'''
    collection.database = database
    line1 = ['evmiles97', 'eve.miles@uw.edu', 'Eve', 'Miles']
    assert collection.add_user(*line1) is False


def test_user_collection_add_user_database_updated(collection, database):
    '''test add_user acctualy updates the database'''
    collection.database = database
    initial_database_length = len(database)
    new_user = ['Big****123', 'AElrick@BTISolutions.com', 'My', 'Secret']
    collection.add_user(*new_user)
    assert collection.database['Big****123']
    assert len(database) > initial_database_length


def test_user_collection_modify_user_reject_not_existing(collection, database):
    '''test modify_user rejects not existing users'''
    collection.database = database
    line1 = ['ClicheKHFan', 'eve.miles@uw.edu', 'Eve', 'Miles']
    result = collection.modify_user(*line1)
    assert result is False


def test_user_collection_modify_user_updated_fields(collection, database):
    '''test modify user changes the user held data'''
    collection.database = database
    new_info = ['evmiles97', 'AElrick@BTISolutions.com', 'My', 'Secret']
    result = collection.modify_user(*new_info)
    assert collection.database['evmiles97'].email == 'AElrick@BTISolutions.com'
    assert collection.database['evmiles97'].user_name == 'My'
    assert collection.database['evmiles97'].user_last_name == 'Secret'
    assert result is True


def test_user_collection_delete_user_reject_not_existing(collection, database):
    '''test delete user rejects not existing users'''
    collection.database = database
    result = collection.delete_user('ClicheKHFan')
    assert result is False


def test_user_collection_delete_user(collection, database):
    '''test user is deleted'''
    collection.database = database
    result = collection.delete_user('evmiles97')
    with pytest.raises(KeyError):
        save = collection.database['evmiles97']
        assert save is None
    assert result is True


def test_user_collection_search_user(collection, database):
    '''test search user returns existing user'''
    collection.database = database
    result = collection.search_user('evmiles97')
    assert result.user_id == 'evmiles97'


def test_user_collection_search_user_not_existing(collection, database):
    '''test search user returns None user'''
    collection.database = database
    result = collection.search_user('ClicheKHFan')
    assert result.user_id is None


# user status tests


def test_user_status_init(impeach):
    '''test UserStatus init'''
    assert impeach.status_id == 'XKPiC6*iW!H3#6'


def test_status_collection_init(status_collection):
    '''test UserStatusCollection init'''
    assert status_collection.database == {}


def test_userstatuscollection_add_status_reject_existing(status_collection, status_database):
    '''test add_status rejects existing status'''
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'
    user_id = 'Hardline_Dem173'
    status_text = 'Impeach Trump!'
    params = [status_id, user_id, status_text]

    assert status_collection.add_status(*params) is False


def test_userstatuscollection_add_status_update_database(status_collection, status_database):
    '''test add_status updates database'''
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'
    user_id = 'Faithless_Floridian'
    status_text = 'God is dead!'
    params = [status_id, user_id, status_text]

    initial_database_length = len(status_database)
    result = status_collection.add_status(*params)

    assert len(status_database) > initial_database_length
    assert status_collection.database['byg8L^qJDjAkR6']
    assert result is True


def test_userstatuscollection_modify_status_reject_not_existing(status_collection, status_database):
    '''test modify_status rejects not existing status'''
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'
    user_id = 'Faithless_Floridian'
    status_text = 'God is dead!'
    params = [status_id, user_id, status_text]

    result = status_collection.modify_status(*params)

    assert result is False


def test_userstatuscollection_modify_status_update_database(status_collection, status_database):
    '''test modify_status updates status data and
    database length does not change.'''
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'
    user_id = 'Faithless_Floridian'
    status_text = 'God is dead!'
    params = [status_id, user_id, status_text]

    initial_database_length = len(status_database)
    result = status_collection.modify_status(*params)
    nietzsche = status_collection.database['XKPiC6*iW!H3#6'].status_text

    assert len(status_database) == initial_database_length
    assert nietzsche == 'God is dead!'
    assert result is True


def test_userstatuscollection_delete_status_reject_not_existing(status_collection, status_database):
    '''test delete_status rejects not existing status'''
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'

    result = status_collection.delete_status(status_id)

    assert result is False


def test_userstatuscollection_delete_status_update_database(status_collection, status_database):
    '''test delete_status updates database'''
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'

    initial_database_length = len(status_database)
    result = status_collection.delete_status(status_id)

    assert len(status_database) < initial_database_length
    assert result is True


def test_userstatuscollection_search_status_reject_not_existing(status_collection, status_database):
    '''test search status rejects not existing status'''
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'

    result = status_collection.search_status(status_id)

    assert result.status_id is None


def test_userstatuscollection_search_status_return_status(status_collection, status_database):
    '''test search status returns status object'''
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'

    initial_database_length = len(status_database)
    result = status_collection.search_status(status_id)

    assert isinstance(result, user_status.UserStatus)
    assert len(status_database) == initial_database_length


# test main


def test_init_user_collection():
    '''test create instance of UserCollection.'''
    collection = main.init_user_collection()

    assert collection.database == {}


def test_init_status_collection():
    '''test create instance of UserStatusCollection'''
    collection = main.init_status_collection()

    assert collection.database == {}


def test_load_users_false(collection):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.

    test load users with incorrect file is false
    '''
    result = main.load_users('missing_fields.csv', collection)

    assert result is False


def test_load_users_true(filename, collection):
    '''test load users with correct file is True'''
    result = main.load_users(filename, collection)

    assert result is True


def test_load_users_ignore_existing(filename, csv_collection):
    '''
    after loading users, the two entry database should become a three entry
    database with no repeated user_ids

    Parameters
    ----------
    filename : str
        accounts.csv
    csv_collection : UserCollection
        database has two entires.

    Returns
    -------
    None.

    '''
    main.load_users(filename, csv_collection)

    loaded_users = []
    for key, _ in csv_collection.database.items():
        loaded_users.append(key)

    for item in loaded_users:
        assert loaded_users.count(item) == 1
    assert len(loaded_users) == 3


def test_save_users_false(collection):
    '''
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    '''
    filename = ' C:by.pyg8 : L^qJ/D-jA.kR6'

    result = main.save_users(filename, collection)

    assert result is False


def test_save_users_true(temp_file, collection):
    '''test save users runs correctly with correct file'''
    
    result = main.save_users(temp_file, collection)

    assert result is True


def test_save_users_existing_file(temp_file, csv_collection):
    '''test save users works with an existing file'''

    main.save_users(temp_file, csv_collection)

    lines = []
    with open(temp_file, 'r') as file:
        lines = file.readlines()

    ref_lines = ['USER_ID,EMAIL,NAME,LASTNAME\n',
                 'evmiles97,eve.miles@uw.edu,Eve,Miles\n',
                 'dave03,david.yuen@gmail.com,David,Yuen']

    comparison = lines == ref_lines
    print('lines:')
    print(lines)
    print('ref_lines:')
    print(ref_lines)

    clean_temp_file()

    assert comparison


def test_load_status_updates_false(status_collection, status_database):
    '''
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    filename = 'missing_fields_status.csv'
    status_collection.database = status_database

    result = main.load_status_updates(filename, status_collection)

    assert result is False


def test_load_status_updates_true(status_collection, status_database):
    '''test load status works with correct file'''
    status_collection.database = status_database

    file = '''STATUS_ID,USER_ID,STATUS_TEXT
evmiles97_00001,evmiles97,"Code is finally compiling"
dave03_00001,dave03,"Sunny in Seattle this morning"
evmiles97_00002,evmiles97,"Perfect weather for a hike"
ted_00002,evmiles97,"Perfect weather for a hike"
ted_moop,ted,"Perfect weather for a hike"'''

    with patch('builtins.open', mock_open(read_data=file)) as mock_file:
        result = main.load_status_updates(mock_file, status_collection)

    assert result is True


def test_load_status_updates_not_exists(status_collection):
    '''test'''
    filename = 'status_updates.csv'
    old_database = copy.copy(status_collection.database)

    result = main.load_status_updates(filename, status_collection)

    assert result is True
    assert status_collection.database != old_database


def test_save_status_updates_false(status_collection):
    '''
    Saves all statuses in status_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    '''
    filename = ' C:by.pyg8 : L^qJ/D-jA.kR6'

    result = main.save_status_updates(filename, status_collection)

    assert result is False


def test_save_status_updates_true(temp_file, status_collection, status_database):
    '''test save status works with correct file'''
    status_collection.database = status_database

    result = main.save_status_updates(temp_file, status_collection)

    clean_temp_file()

    assert result is True


def test_save_status_updates_not_exists(status_collection):
    '''test save status works with empty file'''
    main.save_status_updates('users.csv', status_collection)

    with open('users.csv', 'r') as file:
        text = file.read()

    clean_temp_file('users.csv')

    assert text != ''


def test_add_user_false(tolby, collection, database):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    collection.database = database

    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.add_user(*params)

    assert result is False


def test_add_user_true(tolby, collection):
    '''test add user works with correct values'''
    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.add_user(*params)

    assert result is True


def test_update_user_false(tolby, collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.update_user(*params)

    assert result is False


def test_update_user_true(tolby, collection, database):
    '''test update user works with correct values'''
    collection.database = database

    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.update_user(*params)

    assert result is True


def test_delete_user_false(collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    user_id = 'Cool_kid187'

    result = main.delete_user(user_id, collection)

    assert result is False


def test_delete_user_true(collection, database):
    '''test existing users are deleted'''
    collection.database = database

    user_id = 'Cool_kid187'

    result = main.delete_user(user_id, collection)

    assert result is True


def test_search_user(collection, database):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    '''
    collection.database = database

    user_id = 'Cool_kid187'

    result = main.search_user(user_id, collection)

    assert result.user_id == 'Cool_kid187'

    user_id = 'ClicheKHFan'

    result = main.search_user(user_id, collection)

    assert result is None


def test_add_status_false(stolen, status_collection, status_database):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    status_collection.database = status_database

    user_id = stolen.user_id
    status_id = stolen.status_id
    status_text = stolen.status_text
    params = (user_id, status_id, status_text, status_collection)

    result = main.add_status(*params)

    assert result is False


def test_add_status_true(stolen, status_collection):
    '''test add_status works with correct values'''
    user_id = stolen.user_id
    status_id = stolen.status_id
    status_text = stolen.status_text
    params = (user_id, status_id, status_text, status_collection)

    result = main.add_status(*params)

    assert result is True


def test_update_status_false(stolen, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    user_id = stolen.user_id
    status_id = stolen.status_id
    status_text = stolen.status_text
    params = (status_id, user_id, status_text, status_collection)

    result = main.update_status(*params)

    assert result is False


def test_update_status_true(stolen, status_collection, status_database):
    '''test update status works with correct values'''
    status_collection.database = status_database

    user_id = 'test'
    status_id = stolen.status_id
    status_text = 'test'
    params = (status_id, user_id, status_text, status_collection)

    result = main.update_status(*params)

    assert result is True


def test_delete_status_false(status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    status_id = 'test'

    result = main.delete_status(status_id, status_collection)

    assert result is False


def test_delete_status_true(status_collection, status_database):
    '''test delete_status removes an existing status'''
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'

    result = main.delete_status(status_id, status_collection)

    with pytest.raises(KeyError):
        save = status_collection.database['XKPiC6*iW!H3#6']
        assert save is None
    assert result is True


def test_search_status(status_collection, status_database):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    status_collection.database = status_database
    print(status_collection.database)

    status_id = 'XKPiC6*iW!H3#6'

    result = main.search_status(status_id, status_collection)

    assert result.status_id == 'XKPiC6*iW!H3#6'

    status_id = 'test'

    result = main.search_status(status_id, status_collection)

    assert result is None


if __name__ == '__main__':
    pytest.main(['-v'])
