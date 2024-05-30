import sqlite3
from functools import wraps
from database.user_db.baseclasses import *

USER_DATA_PATH = "database/user_db/user_db.db"


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
    user = Users(cursor.fetchone())

    return user.hash_password == hash_password


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


# add_user(login='customer',
#          hash_password=calculate_sha256_hash('SLB_P@ssw0rd'),
#          role_id=User_role.owner.value)





