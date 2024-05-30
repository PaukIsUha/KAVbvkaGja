from enum import Enum


class User_role(Enum):
    owner = 1
    vendor = 2
    buyer = 3
    user = 4


class Users:
    id: int
    name: str
    hash_password: str
    role_id: int
    count_fields = 4

    def __init__(self, data_arr: tuple):
        if len(data_arr) != self.count_fields:
            raise ValueError('Users constructor invalid array')

        self.id = data_arr[0]
        self.name = data_arr[1]
        self.hash_password = data_arr[2]
        self.role_id = data_arr[3]
