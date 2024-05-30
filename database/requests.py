import sqlite3
from functools import wraps
from database.baseclasses import *

ORACLE_DATA_PATH = "database/oracle_data.db"


def db_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connect = sqlite3.connect(ORACLE_DATA_PATH)
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
        connect = sqlite3.connect(ORACLE_DATA_PATH)
        cursor = connect.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            connect.commit()
            return result
        finally:
            connect.close()

    return wrapper


@db_request
def get_orders(cursor, *args, **kwargs):
    """
    :param cursor: cursor database
    :param args: -
    :param kwargs: -
    :return:
    """
    cursor.execute('''SELECT * FROM orders''')
    return Orders.reinit(cursor.fetchall())


@db_request
def get_orders_last_comment(cursor, *args, **kwargs):
    """
    :param cursor: cursor database
    :param args: -
    :param kwargs: -
    :return:
    """
    cursor.execute('''SELECT o.id, o.order_number, o.PO, o.name, o.vendor, c.comment, c.created
                      FROM orders o
                      LEFT JOIN 
                      (SELECT order_id, comment, created FROM comments 
                            WHERE (order_id, created) IN (SELECT order_id, MAX(created) FROM comments GROUP BY order_id)
                            ) c ON o.id = c.order_id;
                    ''')
    return Orders.reinit(cursor.fetchall())


@db_update
def add_comment(cursor, *args, **kwargs):
    """
    :param cursor: cursor database
    :param args: -
    :param kwargs:
        :k_param order_id: id order
        :k_param comment: new comment value
    :return:
    """
    order_id = kwargs['order_id']
    comment = kwargs['comment']

    cursor.execute('''INSERT INTO comments(order_id, comment) VALUES(?, ?);''', (order_id, comment))
