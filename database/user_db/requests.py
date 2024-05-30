import sqlite3
from functools import wraps
from database.user_db.baseclasses import *
from enum import Enum

USER_DATA_PATH = "database/user_db/user_db.db"


class ERRNO_USERS_DB(Enum):
    ok = 0
    invalid_login = 1
    invalid_password = 2


def db_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connect = sqlite3.connect(USER_DATA_PATH)
        cursor = connect.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            return result
        finally:
            connect.close()

    return wrapper


def db_update(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connect = sqlite3.connect(USER_DATA_PATH)
        cursor = connect.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            connect.commit()
            return result
        finally:
            connect.close()

    return wrapper


@db_request
def isin_users(cursor, *args, **kwagrs):
    """
    :param cursor:
    :param args: -
    :param kwagrs:
        :k_param login: login user
        :k_param hash_password: hash password user
    :return:
    """
    login = kwagrs['login']
    hash_password = kwagrs['hash_password']

    cursor.execute('''SELECT * FROM users WHERE name=?''', (login, ))
    db_user = cursor.fetchone()
    if db_user is None:
        return ERRNO_USERS_DB.invalid_login, None

    user = Users(db_user)

    if user.hash_password == hash_password:
        return ERRNO_USERS_DB.ok, user.role_id
    else:
        return ERRNO_USERS_DB.invalid_password, None


@db_update
def add_user(cursor, *args, **kwagrs):
    """
    :param cursor:
    :param args: -
    :param kwagrs:
        :k_param login: login user
        :k_param hash_password: hash password user
        :k_param role_id: role user
    :return:
    """
    login = kwagrs['login']
    hash_password = kwagrs['hash_password']
    role_id = kwagrs['role_id']

    cursor.execute('''INSERT INTO users(name, hash_password, role_id) VALUES(?, ?, ?)''', (login, hash_password, role_id))


# def calculate_sha256_hash(password):
#     sha256_hash = hashlib.sha256(password.encode()).hexdigest()
#     return sha256_hash
#
#
# add_user(login='test',
#          hash_password=calculate_sha256_hash('1234'),
#          role_id=User_role.user.value)





