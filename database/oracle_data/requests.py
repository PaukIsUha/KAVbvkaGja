import sqlite3
from functools import wraps
from database.oracle_data.baseclasses import *

ORACLE_DATA_PATH = "database/oracle_data/oracle_data.db"


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
        :k_param filters: filters to seq class orders
    :return:
    """
    req_filter = " WHERE "
    filters = kwargs.get('filters')

    for col, value in filters.items():
        if value is not None and value != "":
            if isinstance(value, int):
                req_filter += f"o.{col} = {value} AND "
            else:
                req_filter += f"o.{col} = '{value}' AND "

    if req_filter == " WHERE ":
        req_filter = ""
    else:
        req_filter = req_filter[:-5]

    query = '''
    SELECT o.id, o.order_number, o.PO, o.name, o.vendor, o.quantity,
           o.approval_date, o.promised_date, o.shipped, o.trans_data,
           c.comment, c.created
    FROM orders o
        LEFT JOIN 
        (SELECT order_id, comment, created FROM comments 
            WHERE (order_id, created) IN (SELECT order_id, MAX(created) FROM comments GROUP BY order_id)
        ) c ON o.id = c.order_id''' + req_filter + ";"
    cursor.execute(query)
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


@db_request
def get_unique_col(cursor, *args, **kwargs):
    """
    :param cursor:
    :param args:
    :param kwargs:
        :k_param column - column
    :return: list of unique values
    """
    column = kwargs['column']

    cursor.execute(f"SELECT DISTINCT {column} FROM orders")
    unique_values = [i[0] for i in cursor.fetchall()]
    return unique_values


def get_unique_cols_order():
    return get_unique_col(column='order_number'), get_unique_col(column='po'),\
           get_unique_col(column='name'), get_unique_col(column='vendor')

